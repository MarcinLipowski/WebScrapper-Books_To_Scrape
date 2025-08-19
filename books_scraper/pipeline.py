# books_scraper/pipeline.py
import csv
import logging
import random
import time
import requests
import re
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from .config import CSV_HEADERS, CSV_DELIMITER
from .parse import parse_cards

log = logging.getLogger("books")


def get_table_value(soup, key):
    row = soup.find("th", string = key)
    if row and row.find_next_sibling("td"):
        return row.find_next_sibling("td").get_text(strip=True)
    return None

def parse_available_count(text: str):
    if not text:
        return None
    m = re.search(r"(\d+)", text)
    return int(m.group(1)) if m else None

def scrape(session, start_url: str, out_path: str, max_pages: Optional[int], min_rating: Optional[int], min_price: Optional[float], max_price: Optional[float], detailed: Optional[bool], export_xlsx: Optional[str] = None):
    """
    Fetch paginated catalogue pages, parse rows, dedupe by link, and write CSV.
    """
    page_url = start_url
    page_count = 0
    seen = set()

    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=CSV_DELIMITER)
        writer.writerow(CSV_HEADERS)

        while True:
            page_count += 1
            try:
                resp = session.get(page_url, timeout=10)
                resp.raise_for_status()
            except Exception as err:
                log.error("Failed to fetch %s: %s", page_url, err)
                break

            # Decode & parse
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "lxml")

            status_el = soup.select_one("li.current")
            status = status_el.get_text(strip=True) if status_el else ""
            log.info("Scraping %s | %s", page_url, status)

            # Extract rows
            for row in parse_cards(soup, page_url):
                # Filter by min rating (if provided)
                if (min_rating is not None) and (row["rating_value"] is not None) and (row["rating_value"] < min_rating):
                    continue

                price_val = row["price_val"]
                if (min_price is not None) and (price_val is not None) and (price_val < min_price):
                    continue

                if (max_price is not None) and (price_val is not None) and (price_val > max_price):
                    continue

                link = row["book_link"]
                if link in seen:
                    continue
                seen.add(link)

                upc = None
                stock = None

                if detailed:
                    try:
                        dresp = session.get(link, timeout=10)
                        dresp.raise_for_status()
                        dresp.encoding = "utf-8"
                        dsoup = BeautifulSoup(dresp.text, "lxml")

                        upc_text = get_table_value(dsoup, "UPC")
                        stock_text = get_table_value(dsoup, "Availability")
                        upc = upc_text
                        stock = parse_available_count(stock_text)
                    except requests.RequestException as err:
                        log.error("Failed to fetch %s: %s", link, err)

                writer.writerow([
                    row["title"],
                    row["currency"],
                    row["price_val"],
                    row["rating_value"],
                    row["book_link"],
                    upc,
                    stock,
                ])

            # Stop if page limit reached
            if (max_pages is not None) and (page_count >= max_pages):
                log.info("Reached max pages limit (%s)", max_pages)
                break

            # Follow "next"
            next_link = soup.select_one("li.next a")
            if not next_link:
                break
            page_url = urljoin(page_url, next_link["href"])

            # Polite delay with jitter
            time.sleep(0.5 + random.random() * 0.5)
    log.info("Done! Pages scraped: %s | Rows: %s", page_count, len(seen))

    if export_xlsx:
        try:
            import pandas as pd
            log.info("Exporting CSV -> %s", export_xlsx)
            df = pd.read_csv(out_path, sep=";")
            df.to_excel(export_xlsx, index=False)
            log.info("Exported to %s", export_xlsx)
        except ImportError:
            log.error("pandas/openpyxl not installed. Run pip install pandas openpyxl")

