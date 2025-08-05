# OpenFoodFacts Product Data Updater : update_off_product_data.py

Automates updates to product information on [OpenFoodFacts](https://world.openfoodfacts.org/) via its write API.

## Overview

This script allows:

- **Adding category tags**: breeding types and egg calibers
- **Updating quantity fields**: replaces existing value
- Batch processing from CSV files
- Single-product test mode
- Optional barcode existence verification

## Setup

Install dependencies using:

```bash
uv pip install --group dev
```

## Run


```bash
python update_product_data.py [options]
```

### Batch Mode

```bash
python update_product_data.py --breeding --file breeding.csv
python update_product_data.py --caliber --file caliber.csv
python update_product_data.py --quantity --file quantity.csv
```

### Test Mode (Single Product)

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
```

## CSV Format

- Files must be placed in the `./data/` directory.
- Required columns: `barcode`, `tag`
- Supported delimiters: `,` or `;`

Example:

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

## Behavior

- `--breeding` and `--caliber`: tags are **added** to the category list.
- `--quantity`: field is **replaced**.

### Accepted tag values

#### Breeding:

- `en:eggs`
- `en:chicken-eggs`
- `en:cage-chicken-eggs`
- `en:barn-chicken-eggs`
- `en:free-range-chicken-eggs`
- `en:organic-eggs`

#### Caliber:

- `en:small-eggs`
- `en:medium-eggs`
- `en:large-eggs`
- `en:extra-large-eggs`

#### Quantity:

- Format: `"number pcs"` (e.g., `12 pcs`)

## API Details

- **GET (check barcode)**
  `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`

- **POST (submit update)**
  `https://world.openfoodfacts.org/cgi/product_jqm2.pl`

## Barcode Verification

- Enabled by default.
- Verifies all barcodes via API before updating.
- Throttled: max ~100 requests/min (0.6s delay per request)
- To skip verification, use `--no-verify-barcodes`

> ⚠️ If you disable verification, products with unknown barcodes will be **created** in OpenFoodFacts.

## Authentication

You must provide **OpenFoodFacts account credentials**.

Options:

- CLI args: `--username`, `--password`
- Prompted interactively if not provided
