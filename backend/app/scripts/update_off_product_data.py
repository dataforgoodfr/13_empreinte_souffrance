"""
OpenFoodFacts Product Data Updater

Automates updates of product info in OpenFoodFacts.
Includes batch processing and single test updates.

Usage examples:
  python update_product_data.py --breeding --file breeding.csv
  python update_product_data.py --caliber --file caliber.csv
  python update_product_data.py --quantity --file quantity.csv
  python update_product_data.py --test-breeding --barcode 0061719011930 --tag "en:barn-chicken-eggs"
  python update_product_data.py --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
  python update_product_data.py --test-quantity --barcode 0061719011930 --tag "12 pcs"
"""

import argparse
import csv
import getpass
import os
import sys
import time
from typing import Dict, Optional

import pandas as pd
import requests

# =============================================================================
# CONFIGURATION
# =============================================================================


class Config:
    """
    Configuration constants for the OpenFoodFacts updater script.
    """

    OFF_API_WRITE_URL = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
    OFF_API_GET_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"
    DATA_DIR = "data/"
    REQUEST_DELAY = 0.6  # Fixed delay for ~100 requests/minute
    EGG_TAGS = {
        "en:eggs",
        "en:fresh-eggs",
        "en:chicken-eggs",
        "en:liquid-eggs",  # to be added to taxonomy
        "en:powdered-eggs",  # to be added to taxonomy
        "en:egg-yolk",
        "en:egg-white",
        "en:boiled-eggs",
        "en:pickled-eggs",  # to be added to taxonomy
    }

    BREEDING_TAGS = {
        "en:eggs",
        "en:chicken-eggs",
        "en:cage-chicken-eggs",
        "en:barn-chicken-eggs",
        "en:free-range-chicken-eggs",
        "en:organic-eggs",  # to be added to taxonomy and changed to organic-chicken-eggs
    }
    CALIBER_TAGS = {
        "en:small-eggs",
        "en:medium-eggs",
        "en:large-eggs",
        "en:extra-large-eggs",
    }


# =============================================================================
# UTILS & VALIDATION
# =============================================================================


def load_csv_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load CSV file detecting automatically the delimiter (',' or ';').

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        Optional[pandas.DataFrame]: DataFrame containing the CSV data if loaded successfully,
                                   None if file not found or format error.

    Notes:
        The CSV file must contain at least the columns 'barcode' and 'tag'.
    """
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            sample = csvfile.read(1024)
            csvfile.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;")
            sep = dialect.delimiter

            df = pd.read_csv(csvfile, sep=sep, dtype={"barcode": str, "tag": str})

            if "barcode" not in df.columns or "tag" not in df.columns:
                print("❌ Error: CSV must contain 'barcode' and 'tag' columns")
                return None

            print(f"📊 Loaded {len(df)} products from {file_path} using detected separator '{sep}'")
            return df

    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None


def check_barcode_exists(barcode: str) -> bool:
    """
    Check if a product with the given barcode exists in OpenFoodFacts.

    Args:
        barcode (str): The barcode to check.

    Returns:
        bool: True if the product exists, False otherwise.
    """
    try:
        resp = requests.get(Config.OFF_API_GET_URL.format(barcode), timeout=5)
    except requests.RequestException:
        return False

    if resp.status_code != 200:
        return False

    try:
        data = resp.json()
    except Exception:
        return False

    return data.get("status") == 1


def validate_barcodes_exist(df: pd.DataFrame, delay_seconds: float) -> bool:
    """
    Verify that all barcodes in the DataFrame exist in OpenFoodFacts,
    with a delay between requests to avoid rate limits.

    Args:
        df (pandas.DataFrame): DataFrame containing a 'barcode' column.
        delay_seconds (float): Delay in seconds between API requests.

    Returns:
        bool: True if all barcodes exist, False if any barcode does not exist.
    """
    print(f"🔎 Checking existence of {len(df)} barcodes in OpenFoodFacts (delay {delay_seconds}s)...")
    all_found = True
    for idx, barcode in enumerate(df["barcode"]):
        bc = str(barcode).strip()
        if not check_barcode_exists(bc):
            print(f"❌ Barcode not found in OFF: {bc} (CSV line {idx + 2})")
            all_found = False
        time.sleep(delay_seconds)
    return all_found


def validate_tag_format(tag: str, operation: str) -> bool:
    """
    Validate that a tag is one of the allowed predefined tags
    for a defined operation (breeding, caliber or quantity).
    Quantity tags must be in the format "number unit" (e.g., "12 pcs").
    Breeding and caliber tags must match predefined sets.

    Args:
        tag (str): The tag string.
        operation (str): Either "breeding", "caliber" or "quantity".

    Returns:
        bool: True if the tag is allowed, False otherwise.
    """
    if operation == "breeding":
        return tag.strip() in Config.BREEDING_TAGS

    elif operation == "caliber":
        return tag.strip() in Config.CALIBER_TAGS

    elif operation == "categories":
        categories = [cat.strip() for cat in tag.split(",")]
        return all("en:" in cat for cat in categories)

    elif operation == "quantity":
        parts = tag.strip().split()
        if len(parts) != 2:
            return False
        number, unit = parts
        if not number.isdigit():
            return False
        if unit.lower() != "pcs":
            return False
        return True

    else:
        print(f"❌ Unknown operation: {operation}")
        return False


def validate_tags(df: pd.DataFrame, operation: str) -> bool:
    """
    Validate the 'tag' values in the DataFrame according to the operation type.

    Args:
        df (pandas.DataFrame): DataFrame containing 'tag' column.
        operation (str): Either "breeding" or "quantity".

    Returns:
        bool: True if all tags are valid for the operation, False otherwise.
    """
    all_valid = True
    for idx, tag in enumerate(df["tag"]):
        tag_str = str(tag).strip()
        if not validate_tag_format(tag_str, operation=operation):
            print(f"❌ Invalid {operation} tag '{tag_str}' at CSV line {idx + 2}")
            all_valid = False
    return all_valid


# =============================================================================
# API UPDATE FUNCTIONS
# =============================================================================


def update_product_fields(barcode: str, fields: Dict[str, str], username: str, password: str, comment: str) -> bool:
    """
    Send a POST request to OpenFoodFacts API to update product fields.

    Args:
        barcode (str): Product barcode to update.
        fields (Dict[str, str]): Dictionary of fields to update with their values.
        username (str): OpenFoodFacts username.
        password (str): OpenFoodFacts password.
        comment (str): Comment describing the update.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    try:
        payload = {
            "code": barcode,
            "user_id": username,
            "password": password,
            "comment": comment,
        }
        payload.update(fields)

        response = requests.post(Config.OFF_API_WRITE_URL, data=payload)

        if response.status_code == 403:
            print(f"❌ Error {response.status_code} for {barcode}: Forbidden - check credentials or permissions.")
            return False
        if response.status_code == 404:
            print(f"❌ Error {response.status_code} for {barcode}: API not found")
            return False
        if response.status_code != 200:
            print(f"❌ Error {response.status_code} for {barcode}")
            return False

        print(f"✅ Update successful for {barcode}")
        return True

    except Exception as e:
        print(f"❌ Exception for product {barcode}: {e}")
        return False


def add_category_to_product(barcode: str, category: str, username: str, password: str) -> bool:
    """
    Add a category tag to a product via the API.

    Args:
        barcode (str): Product barcode.
        category (str): Category tag to add.
        username (str): OpenFoodFacts username.
        password (str): OpenFoodFacts password.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return update_product_fields(
        barcode, {"add_categories": category}, username, password, comment="Automated category addition via script"
    )


def update_product_quantity(barcode: str, quantity: str, username: str, password: str) -> bool:
    """
    Update the 'quantity' field of a product via the API.

    Args:
        barcode (str): Product barcode.
        quantity (str): Quantity value to set (e.g., "12 pcs").
        username (str): OpenFoodFacts username.
        password (str): OpenFoodFacts password.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return update_product_fields(
        barcode, {"quantity": quantity}, username, password, comment="Automated quantity update via script"
    )


def update_product_categories(barcode: str, categories: str, username: str, password: str) -> bool:
    """
    Update the 'categories' field of a product via the API.

    Args:
        barcode (str): Product barcode.
        categories (str): Comma-separated string of category tags to set,
            like 'en:eggs,en:fresh-eggs,en:chicken-eggs'
        username (str): OpenFoodFacts username.
        password (str): OpenFoodFacts password.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return update_product_fields(
        barcode, {"categories": categories}, username, password, comment="Automated categories update via script"
    )


def batch_process(df: pd.DataFrame, operation: str, username: str, password: str) -> Dict[str, int]:
    """
    Perform batch updates on a list of products for breeding type or quantity.

    Args:
        df (pandas.DataFrame): DataFrame with 'barcode' and 'tag' columns.
        operation (str): Operation to perform: "breeding", "caliber" or "quantity".
        username (str): OpenFoodFacts username.
        password (str): OpenFoodFacts password.

    Returns:
        Dict[str, int]: Dictionary with counts of successes, failures, and total processed.
    """
    success_count = 0
    failed_count = 0

    print(f"🚀 Starting batch {operation} for {len(df)} products...")

    for idx, row in df.iterrows():
        barcode = str(row["barcode"]).strip()
        tag = str(row["tag"]).replace("\n", ",").replace("\r", ",").strip()

        print(f"\n[{idx + 1}/{len(df)}] Processing {barcode}...")

        if operation == "breeding":
            success = add_category_to_product(barcode, tag, username, password)
        elif operation == "caliber":
            success = add_category_to_product(barcode, tag, username, password)
        elif operation == "quantity":
            success = update_product_quantity(barcode, tag, username, password)
        elif operation == "categories":
            success = update_product_categories(barcode, tag, username, password)
        else:
            print(f"❌ Unknown operation: {operation}")
            success = False

        if success:
            success_count += 1
        else:
            failed_count += 1

        time.sleep(Config.REQUEST_DELAY)

    print(f"\n📊 Batch {operation} complete:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📦 Total: {len(df)}")

    return {"success": success_count, "failed": failed_count, "total": len(df)}


# =============================================================================
# CLI & MAIN
# =============================================================================


def get_credentials(args) -> tuple[str, str]:
    """
    Retrieve OpenFoodFacts username and password from CLI arguments,
    environment variables, or user input prompts.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        tuple[str, str]: Tuple of (username, password).
    """
    username = args.username or os.getenv("OFF_USERNAME")
    password = args.password or os.getenv("OFF_PASSWORD")

    if not username:
        username = input("OpenFoodFacts username: ")
    if not password:
        password = getpass.getpass("OpenFoodFacts password: ")

    return username, password


def parse_args():
    """
    Define and parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Update OpenFoodFacts product data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --breeding --file breeding.csv
  %(prog)s --caliber --file caliber.csv
  %(prog)s --quantity --file quantity.csv
  %(prog)s --categories --file categories.csv
  %(prog)s --test-breeding --barcode 0061719011930 --tag "en:organic-eggs"
  %(prog)s --test-caliber --barcode 0061719011930 --tag "en:large-eggs"
  %(prog)s --test-quantity --barcode 0061719011930 --tag "12 pcs"
  %(prog)s --test-categories --barcode 0061719011930 --tag "en:eggs,en:fresh-eggs,en:chicken-eggs"
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--breeding", action="store_true", help="Add breeding type category")
    group.add_argument("--caliber", action="store_true", help="Add caliber category")
    group.add_argument("--quantity", action="store_true", help="Update product quantity")
    group.add_argument("--categories", action="store_true", help="Update full categories list")
    group.add_argument("--test-breeding", action="store_true", help="Test breeding type add on single product")
    group.add_argument("--test-caliber", action="store_true", help="Test caliber add on single product")
    group.add_argument("--test-quantity", action="store_true", help="Test quantity update on single product")
    group.add_argument("--test-categories", action="store_true", help="Test categories update on single product")

    parser.add_argument("--file", type=str, help="CSV file path for batch operations")
    parser.add_argument("--barcode", type=str, help="Barcode for test operations")
    parser.add_argument("--tag", type=str, help="Tag/value for test operations")
    parser.add_argument("--username", type=str, help="OpenFoodFacts username (or set OFF_USERNAME env var)")
    parser.add_argument("--password", type=str, help="OpenFoodFacts password (or set OFF_PASSWORD env var)")

    parser.add_argument(
        "--verify-barcodes",
        dest="verify_barcodes",
        action="store_true",
        default=True,
        help="Verify that barcodes exist in OpenFoodFacts before processing (default: True)",
    )
    parser.add_argument(
        "--no-verify-barcodes",
        dest="verify_barcodes",
        action="store_false",
        help="Disable barcode existence verification (product will be created if barcode does not exist)",
    )

    return parser.parse_args()


def main():
    """
    Main entry point of the script.
    Handles argument parsing, input validation, credential retrieval,
    and dispatching batch or test update operations.
    """
    args = parse_args()

    # Batch operation flow
    if args.breeding or args.quantity or args.caliber or args.categories:
        if not args.file:
            print("❌ Error: --file required for batch operations")
            sys.exit(1)

        csv_path = os.path.join(Config.DATA_DIR, args.file)
        df = load_csv_data(csv_path)
        if df is None:
            sys.exit(1)

        if args.breeding:
            operation = "breeding"
        elif args.caliber:
            operation = "caliber"
        elif args.categories:
            operation = "categories"
        else:
            operation = "quantity"

        # Validate tags before credentials input
        if not validate_tags(df, operation):
            sys.exit(1)

        # Verify barcodes existence before credentials input (if enabled)
        if args.verify_barcodes:
            if not validate_barcodes_exist(df, Config.REQUEST_DELAY):
                print("❌ One or more barcodes do not exist in OpenFoodFacts. Aborting.")
                sys.exit(1)

        username, password = get_credentials(args)

        if not username or not password:
            print("❌ Error: OpenFoodFacts credentials required")
            sys.exit(1)

        print(f"\n⚠️  About to process {len(df)} products")

        if not args.verify_barcodes:
            print("⚠️ Warning: Barcode existence verification is DISABLED.")
            print("   Products with nonexistent barcodes will be CREATED if they do not exist.\n")

        confirm = input("Type 'CONFIRM' to proceed: ")
        if confirm != "CONFIRM":
            print("Operation cancelled")
            sys.exit(0)

        batch_process(df, operation, username, password)

    # Single test operation flow
    elif args.test_breeding or args.test_quantity or args.test_caliber or args.test_categories:
        if not args.barcode or not args.tag:
            print("❌ Error: --barcode and --tag required for test operations")
            sys.exit(1)

        # Verify barcode existence for tests
        if not check_barcode_exists(args.barcode):
            print(f"❌ Barcode {args.barcode} does not exist in OpenFoodFacts. Aborting.")
            sys.exit(1)

        # Validate tag format before credentials
        if args.test_breeding and not validate_tag_format(args.tag, operation="breeding"):
            print(f"❌ Invalid breeding tag '{args.tag}'")
            sys.exit(1)
        if args.test_caliber and not validate_tag_format(args.tag, operation="caliber"):
            print(f"❌ Invalid caliber tag '{args.tag}'")
            sys.exit(1)
        if args.test_quantity and not validate_tag_format(args.tag, operation="quantity"):
            print(f"❌ Invalid quantity tag '{args.tag}'")
            sys.exit(1)
        if args.test_categories and not validate_tag_format(args.tag, operation="categories"):
            print(f"❌ Invalid categories tag '{args.tag}'")
            sys.exit(1)

        # Get credentials
        username, password = get_credentials(args)

        if not username or not password:
            print("❌ Error: OpenFoodFacts credentials required")
            sys.exit(1)

        # Perform the update operation
        if args.test_breeding or args.test_caliber:
            add_category_to_product(args.barcode, args.tag, username, password)
        elif args.test_quantity:
            update_product_quantity(args.barcode, args.tag, username, password)
        elif args.test_categories:
            update_product_categories(args.barcode, args.tag, username, password)


if __name__ == "__main__":
    main()
