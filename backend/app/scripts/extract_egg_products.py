import argparse
import datetime
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import requests

from app.enums.open_food_facts.product_type_enums import ProductTypePatternRepository


class Config:
    """
    Configuration constants for the egg product extraction script.
    """

    SOURCE_PARQUET = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet"

    DATA_PATH = Path("data")
    LOCAL_PARQUET = DATA_PATH / "food.parquet"
    CSV_PATH = DATA_PATH / "eggs_from_parquet.csv"
    POTENTIAL_CSV_PATH = DATA_PATH / "potential_eggs_from_parquet.csv"
    COLS_TO_JSON_PATH = DATA_PATH / "cols_to_json.txt"

    EXPORT_TIME_BASIC = "~1 min 30 sec"
    EXPORT_TIME_POTENTIAL = "~10 min"

    EGG_CATEGORY = "en:eggs"

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


class PatternRepository:
    """
    Pattern repository for egg product extraction
    Contains patterns to help identify potential eggs
    """

    # SQL pattern to match product names containing eggs when searching potential eggs
    EGG_PATTERN_SQL = "(^|[^A-Za-z])(?:eggs?|oeufs?|uove|huevos?)([^A-Za-z]|$)"

    # List of words that should not be in the product name when searching potential eggs
    EXCLUDED_WORDS = ProductTypePatternRepository.EXCLUDED_WORDS | {
        "coque",
        "starters?",
        "suisses?",
        "con huevo",
        "galettas",
        "pan",
        "gummies",
        "rollos?",
        "omelette?s?",
        "roti",
        "crema",
        "teriyaki",
        "pistache",
        "pie",
        "mix",
        "frito",
        "coffee",
        "al huevo",
        "topping",
        "tofu",
        "barbie",
        "pastas",
        "replacement",
        "nog",
        "boeufs?",
        "encastré",
        "plat",
        "veggie",
        "haribo",
        "marshmallow",
        "jamon",
        "pappardelle",
        "chile",
        "linguine",
        "tarts?",
        "choccy",
        "unicorn",
        "candy",
        "pork",
        "mayonnaises?",
        "bites",
        "petillant",
        "tagliolini",
        "galore",
        "fettucc?ine",
        "dye",
        "leche",
        "lompia",
        "sugar",
        "wheat",
        "good",
        "gianduja",
        "patatas",
        "ciabatta",
        "dove",
        "guimauve",
        "lindt",
        "soup",
        "happy",
        "golden",
        "ozmo",
        "sucreries?",
        "twix",
        "vegetable",
        "vegi",
        "fruite",
        "peanut",
        "avocado",
        "etoiles?",
        "bagels?",
        "pochés?",
        "daim",
        "patties?",
        "rosquillos?",
        "vegetal",
        "setas?",
        "confiseurs?",
        "natillas?",
        "steak",
        "butifarra",
        "tiny",
        "cheddar",
        "spinach",
        "trufados",
        "bun",
        "ham",
        "licornes?",
        "bechamel",
        "nibbly",
        "chorizo",
        "fusilli",
        "cream",
        "mallow",
        "breakfast",
        "crispy?",
        "scotchmallow",
        "marmotte",
        "blancs? d oeufs?",
        "sauces?",
        "wich",
        "plant",
        "replacer",
        "pastry",
        "grill",
        "pains?",
        "salsa",
        "peinture",
        "peppermint",
        "croquants?",
        "mousse",
        "fruits?",
        "cake",
        "tomato",
        "salad",
        "cashew",
        "mushroom",
        "sin huevo",
        "cigogne",
        "taco",
        "aux oeufs",
        "macaroni",
        "custard",
        "bread",
        "barley",
        "you",
        "benedict",
        "tortas?",
        "tortilla",
    }

    EXCLUDED_PATTERNS = re.compile(
        r"\b(" + r"|".join([term.replace(" ", r"\s+") for term in EXCLUDED_WORDS]) + r")\b", re.VERBOSE
    )


def normalize_string(s):
    """
    Function that normalizes a string
    :param s: string to normalize
    :return: normalized string
    """
    if s is None:
        return ""
    s = str(s)
    # removes accents
    s = s.join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    # Unicode normalization
    s = unicodedata.normalize("NFKD", s)
    # replace any punctuation with a space
    s = re.sub(r"[^\w\s]", " ", s)
    # replace digits with a space
    s = re.sub(r"\d+", " ", s)
    # convert uppercase letters to lowercase
    s = s.lower()
    # replace œ with oe
    s = re.sub(r"œ", "oe", s)
    return s


def download_parquet():
    """
    Download the Parquet file from the remote source URL to the local path.

    The file is streamed in chunks with a progress bar displayed in the console.
    If the parent directories do not exist, they are created.

    Effects:
        Creates a 4 GO local Parquet file in the data directory.
    """
    Config.LOCAL_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(Config.SOURCE_PARQUET, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("Content-Length", 0))
        chunk_size = 8192
        downloaded = 0
        with open(Config.LOCAL_PARQUET, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    done = int(50 * downloaded / total_size) if total_size else 0
                    percent = (downloaded / total_size * 100) if total_size else 0
                    bar = "=" * done + " " * (50 - done)
                    print(f"\rDownloading: [{bar}] {percent:.2f}%", end="")
    print(f"\nFile downloaded: {Config.LOCAL_PARQUET}")


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
    Only columns listed in SELECTED_COLUMNS are selected (usefull for further data analysis)

    Returns:
        pandas.DataFrame: Filtered DataFrame with hen egg products.
    """
    query = f"""
    SELECT {",".join(Config.SELECTED_COLUMNS)}
    FROM '{Config.LOCAL_PARQUET}'
    WHERE array_contains(categories_tags, '{Config.EGG_CATEGORY}')
    """
    print("Starting combined DuckDB query to select and filter data...")
    start_time = time.time()
    df = duckdb.execute(query).df()
    print(f"Query executed in {time.time() - start_time:.2f} seconds, rows fetched: {len(df)}")
    return df


def create_df_of_potential_eggs() -> pd.DataFrame:
    """
    Perform a DuckDB SQL query to load and filter the Parquet dataset.
    Filters products to those NOT containing 'en:eggs' in their categories,
    but that could be eggs : 'egg' pattern in their name and no exxcluded categories
    Only columns listed in SELECTED_COLUMNS are selected (usefull for further data analysis)

    Returns:
        pandas.DataFrame: Filtered DataFrame with hen egg products.
    """

    # exécuter la requête DuckDB
    con = duckdb.connect()

    sql = f"""SELECT {",".join("f." + col for col in Config.SELECTED_COLUMNS)}, u.unnest.lang, u.unnest.text
    FROM parquet_scan('{Config.LOCAL_PARQUET}') AS f
    LEFT JOIN UNNEST(f.product_name) AS u ON TRUE
    WHERE (f.categories_tags IS NULL OR NOT array_contains(categories_tags, '{Config.EGG_CATEGORY}'))
    AND u.unnest.lang = 'main'
    AND REGEXP_MATCHES(u.unnest.text, '{PatternRepository.EGG_PATTERN_SQL}', 'i');
    """

    start_time = time.time()
    print(f"Starting combined DuckDB query to select and filter data at {time.strftime('%H:%M:%S')}...")
    df = con.execute(sql).fetchdf()
    print(f"Query executed in {time.time() - start_time:.2f} seconds, rows fetched: {len(df)}")
    print(f"Number of columns returned by duckdb: {len(df.columns)}")

    df = df[
        ~df["text"].apply(lambda x: normalize_string(x)).str.contains(PatternRepository.EXCLUDED_PATTERNS, na=False)
    ]
    print(f"Number of rows after removing excluded patterns: {len(df)}")

    return df


def export_df_as_csv(df, output_path: Path):
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

    Config.DATA_PATH.mkdir(parents=True, exist_ok=True)

    with open(Config.COLS_TO_JSON_PATH, "w") as f:
        json.dump(cols_to_convert, f)

    df.to_csv(output_path, index=False)
    print(f"Export completed: {output_path}")


def remove_parquet_file():
    """
    Remove the local Parquet file if it exists.
    """
    if Config.LOCAL_PARQUET.exists():
        Config.LOCAL_PARQUET.unlink()
        print(f"File deleted: {Config.LOCAL_PARQUET}")
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
    parser.add_argument("--potential", action="store_true", help="Export potential eggs without asking")
    args = parser.parse_args()

    if args.download:
        download_parquet()
    else:
        if not Config.LOCAL_PARQUET.exists():
            answer = (
                input(f"{Config.LOCAL_PARQUET} not found. Do you want to download it now (~ 4 GO) ? (y/n): ")
                .strip()
                .lower()
            )
            if answer == "y":
                download_parquet()
            else:
                sys.exit("Parquet file required. Exiting.")
        else:
            mod_time = file_modification_time(Config.LOCAL_PARQUET)
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            if mod_time.startswith(today_str):
                print(f"Local Parquet file found and up-to-date (last modified: {mod_time}).")
            else:
                answer = (
                    input(
                        f"Local Parquet file found: {Config.LOCAL_PARQUET} (last modified: {mod_time}). "
                        "Do you want to download the newest version (~ 4 GO) ? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if answer == "y":
                    download_parquet()

    # Parse csv_export argument and reask user if not provided
    csv_export = args.csv_export

    if args.potential:
        export_time = Config.EXPORT_TIME_POTENTIAL
    else:
        export_time = Config.EXPORT_TIME_BASIC

    if not csv_export:
        answer = (
            input(f"Do you want to create a new filtered CSV export from the Parquet file? ({export_time}) (y/n): ")
            .strip()
            .lower()
        )
        csv_export = answer == "y"

    if csv_export:
        print(f"Exporting csv ({export_time}) starting at {time.strftime('%H:%M:%S')}...")
        if args.potential:
            df = create_df_of_potential_eggs()
            export_df_as_csv(df, Config.POTENTIAL_CSV_PATH)
        else:
            df = create_filtered_df()
            export_df_as_csv(df, Config.CSV_PATH)
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
