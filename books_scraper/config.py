# books_scraper/config.py

BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"

USER_AGENT = "BooksScraper/1.0 (+https://github.com/MarcinLipowski/WebScrapper-Books_To_Scrape)"

CSV_DELIMITER = ";"
CSV_HEADERS = ["TITLE", "CURRENCY", "PRICE_VALUE", "RATING", "BOOK_LINK", "UPC", "AVAILABLE_COUNT"]

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
