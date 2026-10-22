
import argparse
import csv
import json
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


FIELDS = [
    "name",
    "price",
    "status",
    "shipping",
    "free_returns",
    "items_sold",
]


def get_text(card, selectors):
    """Find the first matching element and return its text."""
    for selector in selectors:
        element = card.select_one(selector)
        if element:
            value = element.get_text(" ", strip=True)
            if value:
                return value
    return None


def money_to_cents(text):
    """Convert a dollar price into an integer number of cents."""
    if text is None:
        return None

    match = re.search(r"\$\s*([\d,]+)(?:\.(\d{1,2}))?", text)
    if not match:
        return None

    dollars = int(match.group(1).replace(",", ""))
    cents = (match.group(2) or "0").ljust(2, "0")
    return dollars * 100 + int(cents)


def parse_shipping(text):
    """Return shipping cost in cents, or None if unknown."""
    if text is None:
        return None

    if "free" in text.lower():
        return 0

    return money_to_cents(text)


def parse_returns(text):
    """Determine whether a listing offers free returns."""
    if text is None:
        return None

    return "free returns" in text.lower()


def parse_sold(text):
    """Extract the number of items sold."""
    if text is None:
        return None

    match = re.search(r"([\d,]+)\s*(?:\+)?\s*sold", text, re.I)
    if match:
        return int(match.group(1).replace(",", ""))

    return None


def extract_items(html):
    """Extract all listing dictionaries from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("li.s-item, div.s-item")

    items = []

    for card in cards:
        name = get_text(card, [
            ".s-item__title",
            "[class*='s-item__title']",
        ])

        if not name or name.lower() == "shop on ebay":
            continue

        price_text = get_text(card, [
            ".s-item__price",
            "[class*='s-item__price']",
        ])

        status = get_text(card, [
            ".SECONDARY_INFO",
            ".s-item__subtitle",
            ".s-item__condition",
        ])

        shipping_text = get_text(card, [
            ".s-item__shipping",
            ".s-item__logisticsCost",
            "[class*='shipping']",
        ])

        returns_text = get_text(card, [
            ".s-item__freeReturns",
            "[class*='freeReturns']",
            "[class*='returns']",
        ])

        sold_text = get_text(card, [
            ".s-item__hotness",
            ".s-item__quantitySold",
            "[class*='sold']",
        ])

        item = {
            "name": name,
            "price": money_to_cents(price_text),
            "status": status,
            "shipping": parse_shipping(shipping_text),
            "free_returns": parse_returns(returns_text),
            "items_sold": parse_sold(sold_text),
        }

        items.append(item)

    return items


def load_page(search, page_number, pages_dir=None):
    """Get HTML from a practice file or from eBay."""

    if pages_dir:
        filename = Path(pages_dir) / f"page-{page_number}.html"
        return filename.read_text(encoding="utf-8")

    response = requests.get(
        "https://www.ebay.com/sch/i.html",
        params={
            "_nkw": search,
            "_pgn": page_number,
        },
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    response.raise_for_status()

    html = response.text

    if "captcha" in html.lower() or "robot check" in html.lower():
        raise RuntimeError("eBay returned a robot check")

    return html


def main():
    parser = argparse.ArgumentParser(
        description="Download eBay search results."
    )

    parser.add_argument("--search", required=True)
    parser.add_argument("--pages-dir")
    parser.add_argument("--csv", action="store_true")

    args = parser.parse_args()

    all_items = []

    for page_number in range(1, 11):
        print(f"Processing page {page_number}...")

        html = load_page(
            args.search,
            page_number,
            args.pages_dir,
        )

        items = extract_items(html)

        if not items:
            raise RuntimeError(
                f"No listings found on page {page_number}. "
                "Check selectors or possible eBay blocking."
            )

        all_items.extend(items)

        if not args.pages_dir and page_number < 10:
            time.sleep(1)

    if args.csv:
        filename = f"{args.search}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(all_items)

    else:
        filename = f"{args.search}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_items, f, indent=2)

    print(f"Saved {len(all_items)} listings to {filename}")


if __name__ == "__main__":
    main()

