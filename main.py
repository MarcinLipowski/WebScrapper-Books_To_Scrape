# scraper.py | Books To Scrape
import requests
from bs4 import BeautifulSoup
import csv

page_to_scrape = requests.get("https://books.toscrape.com/", timeout=10)
page_to_scrape.raise_for_status()
page_to_scrape.encoding = "utf-8"
soup = BeautifulSoup(page_to_scrape.text, "html.parser")

file = open("books.csv", "w", encoding="utf-8-sig", newline="")
writer = csv.writer(file, delimiter=";")

writer.writerow(["TITLES", "PRICE"])

for card in soup.find_all("article", attrs={"class": "product_pod"}):
    title = card.select_one("h3 a")["title"]
    price = card.select_one("p.price_color").get_text(strip=True)
    writer.writerow([title, price])

file.close()
