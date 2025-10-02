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

SOURCE_PARQUET = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet"
DATA_PATH = Path("data")

LOCAL_PARQUET = DATA_PATH / "food.parquet"
CSV_PATH = DATA_PATH / "eggs_from_parquet.csv"

POTENTIAL_CSV_PATH = DATA_PATH / "potential_eggs_from_parquet.csv"
COLS_TO_JSON_PATH = DATA_PATH / "cols_to_json.txt"

EXPORT_TIME_BASIC = "~1 min 30 sec"
EXPORT_TIME_POTENTIAL = "~10 min"

EGG_CATEGORY = "en:eggs"

# SQL pattern to match product names containing eggs when searching potential eggs
EGG_PATTERN_SQL = "(^|[^A-Za-z])(?:eggs?|oeufs?|uove|huevos?)([^A-Za-z]|$)"

# List of words that should not be in the product name when searching potential eggs
EXCLUDED_WORDS = {
    "a la russe",
    "acidule?",
    "after",
    "angelina",
    "assaisonnement",
    "assortis?",
    "aux oeufs",
    "avec",
    "bacon",
    "baguette",
    "barre",
    "biscuits?",
    "blancs? d oeufs?",
    "boiled",
    "bonbons?",
    "boeufs?",
    "boudoirs",
    "bowl",
    "brioches?",
    "brouillade",
    "brouille",
    "brouilles",
    "bunny",
    "cabillauds?",
    "cacao",
    "cacher",
    "cadbury",
    "cailles?",
    "canard",
    "capelan",
    "caramel",
    "cent ans",
    "cheese",
    "choco",
    "chocolate?s?",
    "circus",
    "cloche",
    "clochettes?",
    "colour(ed)?",
    "comte",
    "coquillettes?",
    "coquilles",
    "coque",
    "cookies",
    "cooked",
    "craquant",
    "crackers?",
    "cremes?",
    "crepes?",
    "croco",
    "crudites?",
    "croustillant",
    "croustillants?",
    "cuillers?",
    "cuits?",
    "cuit",
    "curry",
    "degustation",
    "dessert",
    "dino",
    "dinosaures?",
    "dip",
    "dippy",
    "dragees?",
    "drageifie",
    "duck",
    "durs?",
    "eafit",
    "easter",
    "eclats?",
    "egg white",
    "egg whites?",
    "eggwhite",
    "emu",
    "encastré",
    "epinards",
    "entiers?",
    "etoiles?",
    "faberge",
    "falize",
    "farfalles?",
    "ferrero",
    "feuillete",
    "filled",
    "finettes?",
    "fish",
    "flamme",
    "flan",
    "florentine",
    "fourre",
    "fourres",
    "fried",
    "fruits?",
    "fleurs?",
    "fusilli",
    "fun",
    "funny?",
    "garni",
    "gateaux?",
    "gaufres?",
    "geant",
    "gelee",
    "genoises?",
    "gnocchis?",
    "golden",
    "good",
    "gorgonzola",
    "gourmands?",
    "gourmet",
    "goose",
    "guineafowl",
    "gull",
    "happy",
    "hunt",
    "icelandic",
    "jam",
    "jambon",
    "jaune d",
    "jardin",
    "jazzy",
    "jelly",
    "julienne",
    "kinder",
    "kitkat",
    "knepfle",
    "lactes",
    "lapin",
    "lasagnes?",
    "lait",
    "lentilles",
    "ligne",
    "liqueur",
    "liquides?",
    "liquid",
    "lindor",
    "lompes?",
    "loprofin",
    "lump",
    "lympe",
    "macaroni",
    "madeleine",
    "madeleines?",
    "magiques?",
    "marbré?",
    "marmotte",
    "mars",
    "marzipan",
    "mascarpone",
    "mayonn?aise",
    "mayonnaises?",
    "mafaldine",
    "mayo",
    "m ms?",
    "meat",
    "mendiants?",
    "milka",
    "mini",
    "mimosas?",
    "milk",
    "mix",
    "mollets?",
    "mouettes?",
    "moulage",
    "muges",
    "naproxene",
    "neiges?",
    "nids",
    "noir",
    "noisettes?",
    "noodles?",
    "nougat",
    "nougatines?",
    "nouilles?",
    "omelette?s?",
    "onion",
    "or",
    "oreo",
    "orgran",
    "ostrich",
    "paques?",
    "pain",
    "pains?",
    "panzani",
    "papillons",
    "pastes?",
    "pasteurise??",
    "pastas?",
    "patissier",
    "pates?",
    "pate",
    "patisserie",
    "pavot",
    "peeled",
    "penne",
    "pheasant",
    "pickled",
    "plat",
    "poche?",
    "pochés?",
    "pokemon",
    "pomme",
    "poached",
    "poisson",
    "poussin",
    "prednisolone",
    "preema",
    "printemps",
    "praline?",
    "pralines?",
    "quail",
    "quarts",
    "quatre quarts",
    "quatrequarts",
    "quenelles",
    "ravioli",
    "ravioles?",
    "reese",
    "rice",
    "riz",
    "rocket",
    "rolls?",
    "rubans?",
    "rustic",
    "saumons?",
    "sachet",
    "salades?",
    "salted",
    "sando",
    "sandwich",
    "saumon",
    "sausage",
    "sauces?",
    "savoureux",
    "scotch",
    "scrambled?",
    "servis",
    "smarties",
    "snack",
    "sonic",
    "spaetzle",
    "spaghetti",
    "spatzle",
    "speckled",
    "substitute",
    "substitut",
    "sucres?",
    "sucreries?",
    "sucrés",
    "suisses?",
    "surprises?",
    "sweet",
    "taipei",
    "tagliatelles?",
    "tarallis?",
    "tartes?",
    "tendres?",
    "thon",
    "toblerone",
    "tomates?",
    "tortellini",
    "torsades?",
    "touron",
    "truites?",
    "truffes?",
    "turkey",
    "valeur",
    "vegan",
    "vichy",
    "waitrose",
    "waffles?",
    "wraps?",
    "yolk",
    "you",
    "nog",
    "salad",
    "linguine",
    "al huevo",
    "lompia",
    "bechamel",
    "pork",
    "grill",
    "chorizo",
    "tagliolini",
    "fettucc?ine",
    "bun",
    "cake",
    "jamon",
    "bites",
    "twix",
    "bread",
    "frito",
    "patatas",
    "pastry",
    "candy",
    "roti",
    "tarts?",
    "cheddar",
    "pie",
    "steak",
    "taco",
    "unicorn",
    "licornes?",
    "lindt",
    "haribo",
    "spinach",
    "tofu",
    "vegetable",
    "marshmallow",
    "tortilla",
    "mousse",
    "teriyaki",
    "confiseurs?",
    "tomato",
    "soup",
    "ham",
    "sin huevo",
    "gummies",
    "replacer",
    "daim",
    "barbie",
    "cashew",
    "peanut",
    "peinture",
    "avocado",
    "con huevo",
    "cream",
    "custard",
    "pistache",
    "salsa",
    "ciabatta",
    "galettas",
    "breakfast",
    "butifarra",
    "fruite",
    "wich",
    "pan",
    "galore",
    "scotchmallow",
    "mallow",
    "sugar",
    "natilla",
    "dove",
    "cigogne",
    "lindt",
    "mushroom",
    "rollos?",
    "crema",
    "leche",
    "chile",
    "guimauve",
    "just",
    "peppermint",
    "starters?",
    "patties?",
    "vegi",
    "veggie",
    "trufados",
    "replacement",
    "crispy?",
    "croquants?",
    "tortas?",
    "tiny",
    "mega",
    "choccy",
    "pappardelle",
    "wheat",
    "barley",
    "vegetal",
    "petillant",
    "natillas?",
    "topping",
    "benedict",
    "dye",
    "plant",
    "coffee",
    "galore",
    "bagels?",
    "setas?",
    "rosquillos?",
    "nibbly",
    "ozmo",
    "gianduja",
}


EXCLUDED_PATTERNS = re.compile(
    r"\b(" + r"|".join([term.replace(" ", r"\s+") for term in EXCLUDED_WORDS]) + r")\b", re.VERBOSE
)

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
    Only columns listed in SELECTED_COLUMNS are selected (usefull for further data analysis)

    Returns:
        pandas.DataFrame: Filtered DataFrame with hen egg products.
    """
    query = f"""
    SELECT {",".join(SELECTED_COLUMNS)}
    FROM '{LOCAL_PARQUET}'
    WHERE array_contains(categories_tags, '{EGG_CATEGORY}')
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

    sql = f"""SELECT {",".join("f." + col for col in SELECTED_COLUMNS)}, u.unnest.lang, u.unnest.text
    FROM parquet_scan('{LOCAL_PARQUET}') AS f
    LEFT JOIN UNNEST(f.product_name) AS u ON TRUE
    WHERE (f.categories_tags IS NULL OR NOT array_contains(categories_tags, '{EGG_CATEGORY}'))
    AND u.unnest.lang = 'main'
    AND REGEXP_MATCHES(u.unnest.text, '{EGG_PATTERN_SQL}', 'i');
    """

    start_time = time.time()
    print(f"Starting combined DuckDB query to select and filter data at {time.strftime('%H:%M:%S')}...")
    df = con.execute(sql).fetchdf()
    print(f"Query executed in {time.time() - start_time:.2f} seconds, rows fetched: {len(df)}")
    print(f"Number of columns returned by duckdb: {len(df.columns)}")

    df = df[~df["text"].apply(lambda x: normalize_string(x)).str.contains(EXCLUDED_PATTERNS, na=False)]
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

    DATA_PATH.mkdir(parents=True, exist_ok=True)

    with open(COLS_TO_JSON_PATH, "w") as f:
        json.dump(cols_to_convert, f)

    df.to_csv(output_path, index=False)
    print(f"Export completed: {output_path}")


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
    parser.add_argument("--potential", action="store_true", help="Export potential eggs without asking")
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

    # Parse csv_export argument and reask user if not provided
    csv_export = args.csv_export

    if args.potential:
        export_time = EXPORT_TIME_POTENTIAL
    else:
        export_time = EXPORT_TIME_BASIC

    if not csv_export:
        answer = (
            input(f"Do you want to create a new filtered CSV export from the Parquet file? ({export_time}) (y/n): ")
            .strip()
            .lower()
        )
        csv_export = answer == "y"

    if csv_export:
        print(f"Exporting csv ({export_time})...")
        if args.potential:
            df = create_df_of_potential_eggs()
            export_df_as_csv(df, CSV_PATH)
        else:
            df = create_filtered_df()
            export_df_as_csv(df, POTENTIAL_CSV_PATH)
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
