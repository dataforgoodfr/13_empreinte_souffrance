# OpenFoodFacts Product Data Extraction and Update

This repository contains two Python scripts for working with OpenFoodFacts data:

1. **extract_egg_products.py**: Extract and filter products from the "eggs" category from the OpenFoodFacts database exported in Parquet format
2. **update_off_product_data.py**: Upload quantity and farming method product data to OpenFoodFacts via the write API.

## Dependencies

Install dependencies with:

```bash
uv pip install --group dev
```

---

## 1. extract_egg_products.py

### Description

This script downloads a large Parquet file (~4 GB) containing the OpenFoodFacts product database, filters products corresponding to chicken eggs (category **en:eggs**), and exports this data in CSV format.
The parquet, csv and txt data are stored in the data/ folder

### Main Features

- Optional download of the **food.parquet** file from Hugging Face **https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet**.
- Filtering with DuckDB of products containing the `en:eggs` category, excluding certain categories not related to chicken eggs (e.g.: **en:duck-eggs**, **en:meals**).
- Export to an **eggs_from_parquet.csv** file with JSON serialization of complex columns.
- Export of columns in JSON format to a **cols_to_json.txt** file to facilitate subsequent CSV import
- Optional deletion of the local Parquet file.

### Usage

```bash
python extract_egg_products.py [--download] [--remove] [--csv-export]
```

Options:

- `--download`: downloads the Parquet file before processing.
- `--remove`: removes the Parquet file after export.
- `--csv-export`: directly exports the filtered CSV without asking.
Prompted interactively if not provided

### Examples

- Download the Parquet file and export the CSV, keep the Parquet file for reuse:

```bash
python extract_egg_products.py --download --csv-export
```

- Export the CSV from an existing Parquet file from an already stored and preserved parquet file:

```bash
python extract_egg_products.py --csv-export
```

- To retrieve the latest product data without cluttering disk space: download the Parquet file, export the csv and delete the Parquet file:

```bash
python extract_egg_products.py --download --csv-export --remove
```
---

## 2. OpenFoodFacts Product Data Update Script: update_off_product_data.py

Automates product data updates on [OpenFoodFacts](https://world.openfoodfacts.org/) via the write API.

### Overview

The script allows:

- Adding category tags: breeding types and egg calibers
- Updating quantity fields: replaces existing value
- Batch processing from CSV files
- Single-product test mode
- Optional barcode existence verification


### Running the Script

```bash
python update_product_data.py [options]
```

#### Batch Update

```bash
python update_product_data.py --breeding --file breeding.csv
python update_product_data.py --caliber --file caliber.csv
python update_product_data.py --quantity --file quantity.csv
```

#### Single Product Test

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
```

### CSV Format

- Files must be placed in the `./data/` directory.
- Required columns: `barcode`, `tag`
- Supported delimiters: `,` or `;`

Example:

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

### Operation Behavior

- `--breeding` and `--caliber`: tags are added to the category list.
- `--quantity`: field is replaced

#### Valid Tags

##### Farming Method:

- `en:eggs`
- `en:chicken-eggs`
- `en:cage-chicken-eggs`
- `en:barn-chicken-eggs`
- `en:free-range-chicken-eggs`
- `en:organic-eggs`

##### Size:

- `en:small-eggs`
- `en:medium-eggs`
- `en:large-eggs`
- `en:extra-large-eggs`

##### Quantity:

- Format: `"{number} pcs"` (e.g. `12 pcs`)

### API Used

- **GET** (barcode verification):
  `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`

- **POST** (update):
  `https://world.openfoodfacts.org/cgi/product_jqm2.pl`

### Barcode Verification

- Enabled by default.
- Verifies all barcodes via API before updating.
- Throttled: max ~100 requests/min (0.6s delay per request)
- To skip verification, use `--no-verify-barcodes`

> ⚠️ If you disable verification, products with unknown barcodes will be created in OpenFoodFacts.

### Required Authentication

You must provide **OpenFoodFacts account credentials**.

Options:

- CLI args: `--username`, `--password`
- Prompted interactively if not provided
