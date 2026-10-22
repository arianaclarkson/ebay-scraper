
## CSV Extra Credit

The scraper supports an optional `--csv` flag. When this
flag is included, the program saves the search results as
a CSV file instead of a JSON file.

To generate the three CSV files using the practice pages,
run these commands:

```bash
python ebay-dl.py --search "garden tools" --pages-dir practice-pages --csv
python ebay-dl.py --search "laptop" --pages-dir practice-pages --csv
python ebay-dl.py --search "shoes" --pages-dir practice-pages --csv
```

The resulting files are:

- `garden tools.csv`
- `laptop.csv`
- `shoes.csv`

These files contain artificial practice data.

