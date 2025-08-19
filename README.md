# Books to Scrape – Python Scraper

A small, production-style scraper for **books.toscrape.com**.  
Built with `requests` + `BeautifulSoup` and the fast `lxml` parser. Exports a CSV (semicolon-delimited, UTF-8 BOM) and can optionally export to Excel.

## Features
- Paginates via the site’s **Next** button until the last page
- Robust HTTP session with **retries + backoff** and a custom User-Agent
- Fast HTML parsing with **lxml**
- Filters: **min/max price**, **min rating**
- Optional detail enrichment (`--detailed`) to fetch **UPC** and **available stock** from each book’s page
- Optional **Excel export** (`--export-xlsx`)

## Project structure
books_scraper/
init.py
cli.py # argparse + logging entrypoint
config.py # BASE_URL, USER_AGENT, CSV headers/delimiter, rating map
http.py # requests.Session with retries & UA
parse.py # list-page parsing → (title, currency, price, rating, link)
pipeline.py # pagination, filters, (optional) detail fetch, CSV/XLSX export
`cli.py` builds the session and forwards CLI flags into the pipeline. :contentReference[oaicite:0]{index=0}  
Config constants live in `config.py` (headers include `UPC` and `AVAILABLE_COUNT`). :contentReference[oaicite:1]{index=1}  
The HTTP session (retries/backoff) is set up in `http.py`. :contentReference[oaicite:2]{index=2}  
Card parsing is implemented in `parse.py`. :contentReference[oaicite:3]{index=3}  
The main loop, filters, detail fetch (UPC/stock), and export live in `pipeline.py`. :contentReference[oaicite:4]{index=4}

## Install
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```
## Usage
Excel export requires pandas + openpyxl. Install them only if you’ll use --export-xlsx.

Run from the project root as a module:
```bash
python -m books_scraper.cli --out books.csv --max-pages 3 --min-rating 3 --min-price 20 --max-price 60 --log-level INFO
```
## CLI options

`--out` (default: books.csv) – Output CSV path. 

`--max-pages` – Stop after N catalogue pages. 

`--min-rating` – Keep books with rating ≥ N (1–5). 

`--min-price` / `--max-price` – Keep books within a price range (floats). 

`--detailed` – Also fetch each book’s page to extract UPC and available stock (slower). 

`--export-xlsx [name.xlsx]` – Export to Excel. If provided without a value, defaults to books.xlsx. 

`--log-level` – DEBUG|INFO|WARNING|ERROR|CRITICAL.

## Output format
CSV headers:

TITLE; CURRENCY; PRICE_VALUE; RATING; BOOK_LINK; UPC; STOCK

PRICE_VALUE is numeric (float), RATING is 1–5, and BOOK_LINK is absolute. UPC/stock are filled only when --detailed is used.

Excel tip (EU locales): CSV uses a semicolon delimiter and UTF-8 BOM so double-clicking in Excel splits columns correctly.

## Notes & Ethics

This targets Books to Scrape, a site intended for scraping practice. For real sites, always review Terms of Service, respect robots.txt, use a clear User-Agent, set rate limits, and add backoff/retries. The default User-Agent is configured in config.py.

## Roadmap

- List/choose category, and sort results before writing
- SQLite/Parquet sinks with unique keys
- Tests with saved HTML fixtures; CI via GitHub Actions
- JSON output
