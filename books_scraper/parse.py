# books_scraper/parse.py
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .config import RATING_MAP

_price_re = re.compile(r"([£€$])\s*([0-9]+(?:\.[0-9]+)?)")

def parse_cards(soup: BeautifulSoup, base_url: str):
    """
    Yield dict rows for each product card on the page.
    Keys: title, currency, price_val, rating_value, book_link
    """
    for card in soup.find_all("article", class_="product_pod"):
        # Title & link
        a = card.select_one("h3 a")
        if not a:
            continue
        title = a.get("title") or a.get_text(strip=True)
        book_link = urljoin(base_url, a.get("href", ""))

        # Price -> currency + float
        raw_price = card.select_one("p.price_color")
        raw_text = raw_price.get_text(strip=True) if raw_price else ""
        m = _price_re.match(raw_text)
        currency = m.group(1) if m else "£"
        price_val = float(m.group(2)) if m else None

        # Rating -> numeric 1-5
        rating_tag = card.select_one("p.star-rating")
        classes = rating_tag.get("class", []) if rating_tag else []
        rating_word = next((c for c in classes if c != "star-rating"), None)
        rating_value = RATING_MAP.get(rating_word, None)

        yield {
            "title": title,
            "currency": currency,
            "price_val": price_val,
            "rating_value": rating_value,
            "book_link": book_link,
        }
