import argparse
import datetime
import json
import sys
import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import requests

SOURCE_PARQUET = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet"
DATA_PATH = Path("../data")
LOCAL_PARQUET = DATA_PATH / "food.parquet"
CSV_PATH = DATA_PATH / "eggs_from_parquet.csv"


# List of categories to exclude from selected products because pointing to products which are not eggs
EXCLUDED_CATEGORIES = {
    "en:chocolate-eggs",
    "en:duck-eggs",
    "en:easter-eggs",
    "en:fish-eggs",
    "en:free-range-duck-eggs",
    "en:quail-eggs",
    "en:raw-quail-eggs",
    "en:savoury-eggs",
    "en:scotch-eggs",
    "en:streamed-eggs",
    "en:meals",
    "en:snacks",
    "en:meats-and-their-products",
    "en:breads",
}

# List of columns which are useful for further data analysis
SELECTED_COLUMNS = [
    "code",
    "categories_tags",
    "labels_tags",
    "product_name",
    "generic_name",
    "quantity",
    "product_quantity_unit",
    "product_quantity",
    "allergens_tags",
    "ingredients_tags",
    "ingredients",
    "countries_tags",
    "images",
]


def download_parquet():
    """
    Download the Parquet file from the remote source URL to the local path.

    The file is streamed in chunks with a progress bar displayed in the console.
    If the parent directories do not exist, they are created.

    Effects:
        Creates a 4 GO local Parquet file in the data directory.
    """
    LOCAL_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(SOURCE_PARQUET, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("Content-Length", 0))
        chunk_size = 8192
        downloaded = 0
        with open(LOCAL_PARQUET, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(50 * downloaded / total_size) if total_size else 0
                    percent = (downloaded / total_size * 100) if total_size else 0
                    bar = "=" * done + " " * (50 - done)
                    print(f"\rDownloading: [{bar}] {percent:.2f}%", end="")
    print(f"\nFile downloaded: {LOCAL_PARQUET}")


def detect_columns_to_convert(df):
    """
    Identify columns in the DataFrame that contain complex data types
    such as lists, dictionaries, or numpy arrays which require JSON serialization.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.

    Returns:
        list: List of column names containing complex objects.
    """
    cols_to_convert = []
    for col in df.columns:
        sample = df[col].dropna().head(20)
        if sample.apply(lambda x: isinstance(x, (list, dict, np.ndarray))).any():
            cols_to_convert.append(col)
    return cols_to_convert


def ndarray_to_json(arr):
    """
    Serialize complex objects (lists, dicts, numpy arrays) returned by duckdb to JSON strings.
    This ensures that columns containing non-scalar values can be safely exported to CSV.

    Args:
        arr: A single element potentially of type list, dict, numpy.ndarray, or scalar.

    Returns:
        str or original: JSON string if input is list, dict or numpy.ndarray, else the original value.
    """
    if isinstance(arr, (list, dict)):
        return json.dumps(arr)
    elif isinstance(arr, np.ndarray):
        return json.dumps(arr.tolist())
    else:
        return arr


def create_filtered_df() -> pd.DataFrame:
    """
    Perform a DuckDB SQL query to load and filter the Parquet dataset.

    Filters products to those containing 'en:eggs' in their categories,
    excluding products that match any categories in EXCLUDED_CATEGORIES (duck eggs...).

    Only columns listed in SELECTED_COLUMNS are selected (usefull for further data analysis)

    Returns:
        pandas.DataFrame: Filtered DataFrame with hen egg products.
    """
    exclusion_conditions = " AND ".join(f"NOT array_contains(categories_tags, '{cat}')" for cat in EXCLUDED_CATEGORIES)
    query = f"""
    SELECT {",".join(SELECTED_COLUMNS)}
    FROM '{LOCAL_PARQUET}'
    WHERE array_contains(categories_tags, 'en:eggs')
    AND {exclusion_conditions}
    """
    print("Starting combined DuckDB query to select and filter data...")
    start_time = time.time()
    df = duckdb.execute(query).df()
    print(f"Query executed in {time.time() - start_time:.2f} seconds, rows fetched: {len(df)}")
    return df


def export_df_as_csv(df):
    """
    Convert complex columns to JSON strings and export the DataFrame to CSV.
    Saves the list of JSON-converted columns in a text file for reference and new python imports

    Args:
        df (pandas.DataFrame): The DataFrame to export.

    Effects:
        Creates or overwrites '../data/eggs_from_parquet.csv' CSV file.
        Creates or overwrites '../data/cols_to_json.txt' JSON metadata file.
    """
    cols_to_convert = detect_columns_to_convert(df) + ["ingredients"]
    # TODO : search why ingredients is not detected

    cols_to_convert = list(set(cols_to_convert))
    print(f"Columns to convert to JSON: {cols_to_convert}")

    for col in cols_to_convert:
        df[col] = df[col].apply(ndarray_to_json)

    DATA_PATH.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH / "cols_to_json.txt", "w") as f:
        json.dump(cols_to_convert, f)

    df.to_csv(CSV_PATH, index=False)
    print(f"Export completed: {CSV_PATH}")


def remove_parquet_file():
    """
    Remove the local Parquet file if it exists.
    """
    if LOCAL_PARQUET.exists():
        LOCAL_PARQUET.unlink()
        print(f"File deleted: {LOCAL_PARQUET}")
    else:
        print("No Parquet file to delete.")


def file_modification_time(path: Path) -> str:
    """
    Retrieve the last modification time of a file formatted as a string.
    Args:
        path (Path): Path to the file.
    Returns:
        str: Timestamp of last modification in 'YYYY-MM-DD HH:MM:SS' format.
    """
    ts = path.stat().st_mtime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="Extract and filter egg products from the OpenFoodFacts database.")
    parser.add_argument("--download", action="store_true", help="Download the Parquet file before processing")
    parser.add_argument("--remove", action="store_true", help="Delete the Parquet file after export")
    parser.add_argument("--csv-export", action="store_true", help="Export filtered CSV without asking")
    args = parser.parse_args()

    if args.download:
        download_parquet()
    else:
        if not LOCAL_PARQUET.exists():
            answer = (
                input(f"{LOCAL_PARQUET} not found. Do you want to download it now (~ 4 GO) ? (y/n): ").strip().lower()
            )
            if answer == "y":
                download_parquet()
            else:
                sys.exit("Parquet file required. Exiting.")
        else:
            mod_time = file_modification_time(LOCAL_PARQUET)
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            if mod_time.startswith(today_str):
                print(f"Local Parquet file found and up-to-date (last modified: {mod_time}).")
            else:
                answer = (
                    input(
                        f"Local Parquet file found: {LOCAL_PARQUET} (last modified: {mod_time}). "
                        "Do you want to download the newest version (~ 4 GO) ? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if answer == "y":
                    download_parquet()

    if args.csv_export:
        print("Exporting csv (~1 min 30 sec)...")
        df = create_filtered_df()
        export_df_as_csv(df)
    else:
        answer = (
            input("Do you want to create a new filtered CSV export from the Parquet file? (~1 min 30 sec) (y/n): ")
            .strip()
            .lower()
        )
        if answer == "y":
            df = create_filtered_df()
            export_df_as_csv(df)
        else:
            print("Skipping CSV export.")

    if args.remove:
        remove_parquet_file()
    else:
        answer = input("Do you want to delete the local Parquet file? (y/n): ").strip().lower()
        if answer == "y":
            remove_parquet_file()
        else:
            print("Parquet file kept.")


if __name__ == "__main__":
    main()
