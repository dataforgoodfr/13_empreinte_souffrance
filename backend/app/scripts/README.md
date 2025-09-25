# OpenFoodFacts Product Data Extraction and Update

This repository contains three Python scripts for working with OpenFoodFacts data:

1. **extract_egg_products.py**: Extract and filter products from the "eggs" category from the OpenFoodFacts database exported in Parquet format
2. **update_off_product_data.py**: Upload quantity and farming method product data to OpenFoodFacts via the write API
3. **process_product_data.py**: Analysis and processing of egg product data with OCR predictions and farming type calculations
4. **export_computed_data_to_excel.py**: Export processed data to formatted Excel files with images and analysis columns

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
- Replacing entire category lists
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
python update_product_data.py --categories --file categories.csv
```

#### Single Product Test

```bash
python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:barn-chicken-eggs"
python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
python update_product_data.py --test-categories --barcode 0061719011930 --tag "en:eggs,en:chicken-eggs,en:barn-chicken-eggs,en:fresh-eggs,en:large-eggs"
```

### CSV Format

- Files must be placed in the `./data/` directory.
- Required columns: `barcode`, `tag`
- Supported delimiters: `,` or `;`
- Support delimiter for categories updater : `;`

Example:

```csv
barcode,tag
0061719011930,en:free-range-chicken-eggs
```

```csv
barcode,tag
0061719011930;en:free-range-chicken-eggs,en:chicken-eggs,en:eggs
```

```csv
barcode,tag
0061719011930;"en:free-range-chicken-eggs,en:chicken-eggs\nen:eggs"
```


### Operation Behavior

- `--breeding` and `--caliber`: tags are added to the category list.
- `--quantity`: field is replaced
- `--categories`: replaces the entire category list with provided tags

#### Valid Tags

##### Farming Method:

- `en:eggs`
- `en:chicken-eggs`
- `en:cage-chicken-eggs`
- `en:barn-chicken-eggs`
- `en:free-range-chicken-eggs`
- `en:organic-eggs`

##### Caliber:

- `en:small-eggs`
- `en:medium-eggs`
- `en:large-eggs`
- `en:extra-large-eggs`

##### Categories:
All strings starting with `en:` or `fr:` corresponding to OpenFoodFacts category tags.

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

---

## 3. Product Data Analysis and Processing Script: process_product_data.py

### Description

This script processes and analyzes egg product data by combining OpenFoodFacts data with OCR predictions and breeding type calculations from the PainReportCalculator. It generates sunburst chart visualizations to analyze data coverage.

### Main Features

- Loading and parsing of CSV product data with JSON columns
- Automatic calculation of farming types and egg quantities via the `PainReportCalculator`
- Integration of OCR predictions from a JSONL file
- Export of enriched data in CSV format
- French product filtering
- Generation of interactive sunburst charts to visualize data distribution

### Data Structure

The script processes several data sources:

- **Product data**: CSV file `eggs_from_parquet.csv` with JSON columns
- **OCR predictions**: JSONL file containing text extractions and predictions
- **Metadata**: `cols_to_json.txt` file listing columns to parse as JSON

Output files:

- `processed_products.csv`: complete data with farming calculations
- `processed_products_fr.csv`: French products subset

```
ROOT_PATH/
├── analysis/neural_category_predictions/data/
│   └── dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl
└── data/
    ├── eggs_from_parquet.csv
    ├── cols_to_json.txt
    ├── processed_products.csv
    └── processed_products_fr.csv
```

### Quantity and Farming Method Calculation

The script uses the `PainReportCalculator` to extract:

- **Egg count**: automatic counting from product data
- **Caliber**: egg size (small, medium, large, extra-large)
- **Farming type**: farming method (cage, barn, free-range, organic)

Return codes:

- `egg_count = -1`: quantity not found
- `egg_count = -2`: product not handled by calculator
- `caliber = "no caliber"`: caliber not determined
- `breeding = "no breeding"`: farming type not determined
- `caliber/breeding = "not managed"`: product not handled by calculator

### Generated Visualizations

The script generates sunburst charts showing the proportion and number of products for which farming method and quantity were found by the calculator.

Display options:
- With or without caliber inclusion in hierarchy
- **France** or **World** dataset

### Usage

```bash
python process_product_data.py [--dataset {world,france}] [--include-caliber] [--no-plot] [--no-process]
```
Options :
- `--dataset {world,france}`: choice of dataset to visualize (default: france)
- `--include-caliber`: include calibers in the sunburst chart
- `--no-plot`: disable chart display
- `--no-process`: skip processing and load already processed data

#### Examples

```bash
# Processing with default chart (France, without calibers)
python process_product_data.py

# World chart without calibers
python process_product_data.py --dataset world

# French chart with calibers
python process_product_data.py --include-caliber

# Processing only, no display
python process_product_data.py --no-plot

# Display only, no reprocessing (loads already processed data)
python process_product_data.py --no-process --dataset world --include-caliber
```


### Specific Dependencies

- `plotly.express` for sunburst visualizations
- Business module `app.business.open_food_facts.pain_report_calculator`
- Validation schemas `app.schemas.open_food_facts.external.ProductData`

## 4. export_computed_data_to_excel.py

### Description

This script exports product data processed by the calculator (`processed_products(_fr).csv`) to formatted Excel files for data verification.
It automatically adds product data, images, analysis columns (OCR, predictions, breeding types…), and hyperlinks to OpenFoodFacts.

### Main Features

- Load the OpenFoodFacts eggs CSV file after enrichment with calculator + OCR information
- Generate Excel files:
  - **Test**: random sample of `n` products (`test_products.xlsx`)
  - **All products**: the entire CSV (`all_products.xlsx`)
  - **Products with missing information**: products without detected breeding type or quantity (`missing_data_products.xlsx`)
- Hyperlinks to OpenFoodFacts product pages
- Image insertion using Excel formulas (open in Google Sheets to display automatically)

The script can be adapted for a given list of product codes.

### Usage

```bash
# Test mode (random sample)
python backend/app/scripts/export_computed_data_to_excel.py --test

# All products
python backend/app/scripts/export_computed_data_to_excel.py --all-products

# Missing data mode (filtered categories)
python backend/app/scripts/export_computed_data_to_excel.py --missing-data

# To process only French products
python backend/app/scripts/export_computed_data_to_excel.py --all-products --fr


If no argument is provided, the script will offer an interactive mode.

### Input and Output Files

- Input: `backend/app/scripts/data/processed_products(_fr).csv`
- Outputs:
  - `test_products(_fr).xlsx` (test)
  - `all_products(_fr).xlsx` (all products)
  - `missing_data_products(_fr).xlsx` (production with multiple sheets)

### Specific Dependencies

- `pandas`, `numpy`
- `openpyxl` for Excel writing and formatting
- `tqdm` for progress bars
