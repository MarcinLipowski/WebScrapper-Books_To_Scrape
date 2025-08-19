# books_scraper/cli.py
import argparse
import logging
from .config import BASE_URL
from .http import build_session
from .pipeline import scrape


def main():
    ap = argparse.ArgumentParser(description="Scrape books.toscrape.com")
    ap.add_argument("--out", default="books.csv", help="Output CSV file (default: books.csv)")
    ap.add_argument("--max-pages", type=int, default=None, help="Maximum pages to scrape")
    ap.add_argument("--min-rating", type=int, default=None, help="Only keep books with rating >= this (1-5)")
    ap.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    ap.add_argument("--min-price", type=float, default=None, help="Only keep books with price >= this | accepts float")
    ap.add_argument("--max-price", type=float, default=None, help="Only keep books with price <= this | accepts float")
    ap.add_argument("--detailed", type=bool, default=False, help="Scrapes detailed info like UPC and amount in stock. Requires more time full scrape not recommended")
    ap.add_argument("--export-xlsx", nargs="?", const="books.xlsx", help="Export results to Excel (.xlsx). You can additionally provide a filename.")
    args = ap.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s %(message)s")
    session = build_session()

    scrape(session=session, start_url=BASE_URL, out_path=args.out, max_pages=args.max_pages, min_rating=args.min_rating, min_price=args.min_price, max_price=args.max_price, detailed=args.detailed, export_xlsx=args.export_xlsx)


if __name__ == "__main__":
    main()
