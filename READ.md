
# eBay Scraper

## Project Description

This project is a Python web scraper that collects eBay
search results and saves product information as JSON files.

The program extracts the name, price, condition, shipping
cost, free returns status, and number of items sold.

It uses the requests library to download HTML pages and
Beautiful Soup to extract listing information.

The program supports both live eBay pages and saved practice
HTML files.

## Setup

Install the required Python libraries:

```bash
python -m pip install requests beautifulsoup4
```

## Running the Scraper

To run a live eBay search:

```bash
python ebay-dl.py --search "garden tools"
```

If eBay blocks requests, use the provided practice pages.

The following commands generated the three JSON files
included in this repository:

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "laptop" --pages-dir practice-pages
python ebay-dl.py --search "shoes" --pages-dir practice-pages
```

These three JSON files contain artificial practice data,
rather than live eBay results.

## CSV Extra Credit

The program also supports CSV output using the --csv flag.

The following commands generated the three CSV files:

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
python ebay-dl.py --search "laptop" --pages-dir practice-pages --csv
python ebay-dl.py --search "shoes" --pages-dir practice-pages --csv
```

## Project Instructions

https://csci40.rtealwitter.com/projects/02_webscraping/project.html
