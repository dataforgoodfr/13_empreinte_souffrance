#!/usr/bin/env python3
"""
OpenFoodFacts Product Data Updater

Automates updates of product info in OpenFoodFacts.
Includes batch processing and single test updates.

Usage examples:
  python product_data_updater.py --breeding-types --file breeding.csv
  python product_data_updater.py --quantities --file quantities.csv
  python product_data_updater.py --test-breeding --barcode 3760074380089 --tag "en:organic-eggs"
  python product_data_updater.py --test-quantity --barcode 3760074380089 --tag "12 pcs"
"""

import pandas as pd
import requests
import os
import argparse
import sys
import getpass
import time
from typing import Optional, Dict

# =============================================================================
# CONFIGURATION
# =============================================================================

class Config:
    OFF_API_WRITE_URL = "https://world.openfoodfacts.org/cgi/product_jqm2.pl"
    OFF_API_GET_URL = "https://world.openfoodfacts.org/api/v0/product/{}.json"
    DATA_DIR = "../data"
    REQUEST_DELAY = 0.6  # Fixed delay for ~100 requests/minute
    BREEDING_TAGS = {
        "en:eggs",
        "en:chicken-eggs",
        "en:cage-chicken-eggs",
        "en:barn-chicken-eggs",
        "en:free-range-chicken-eggs",
        "en:organic-eggs"
    }

# =============================================================================
# UTILS & VALIDATION
# =============================================================================

def load_csv_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load CSV with ';' separator.
    Requires 'barcode' and 'tag' columns.
    """
    try:
        df = pd.read_csv(file_path, sep=";")
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None

    if 'barcode' not in df.columns or 'tag' not in df.columns:
        print(f"❌ Error: CSV must contain 'barcode' and 'tag' columns")
        return None

    print(f"📊 Loaded {len(df)} products from {file_path}")
    return df

def check_barcode_exists(barcode: str) -> bool:
    """
    Check if barcode exists in OFF via GET request.
    Return True if found, False otherwise.
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
    Verify all barcodes exist on OFF with delay between requests.
    Returns False if any barcode missing.
    """
    print(f"🔎 Checking existence of {len(df)} barcodes in OpenFoodFacts (delay {delay_seconds}s)...")
    all_found = True
    for idx, barcode in enumerate(df['barcode']):
        bc = str(barcode).strip()
        if not check_barcode_exists(bc):
            print(f"❌ Barcode not found in OFF: {bc} (CSV line {idx + 2})")
            all_found = False
        time.sleep(delay_seconds)
    return all_found

def validate_quantity_tag_format(tag: str) -> bool:
    """
    Check if tag matches format 'xx pcs' where xx is an integer.
    """
    parts = tag.strip().split()
    if len(parts) != 2:
        return False
    number, unit = parts
    if not number.isdigit():
        return False
    if unit.lower() != "pcs":
        return False
    return True

def validate_breeding_tag_format(tag: str) -> bool:
    """
    Check if tag is in the allowed breeding tag list.
    """
    return tag.strip() in Config.BREEDING_TAGS

def validate_tags(df: pd.DataFrame, operation: str) -> bool:
    """
    Validate all tags in dataframe according to operation.
    """
    for idx, tag in enumerate(df['tag']):
        tag_str = str(tag).strip()
        if operation == "breeding":
            if not validate_breeding_tag_format(tag_str):
                print(f"❌ Invalid breeding tag '{tag_str}' at CSV line {idx + 2}")
                return False
        elif operation == "quantities":
            if not validate_quantity_tag_format(tag_str):
                print(f"❌ Invalid quantity tag '{tag_str}' at CSV line {idx + 2}")
                return False
    return True

# =============================================================================
# API UPDATE FUNCTIONS
# =============================================================================

def update_product_fields(
    barcode: str,
    fields: Dict[str, str],
    username: str,
    password: str,
    comment: str
) -> bool:
    """
    POST update product fields to OpenFoodFacts API.
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
    Add category tag to product.
    """
    return update_product_fields(
        barcode,
        {"add_categories": category},
        username,
        password,
        comment="Automated category addition via script"
    )

def update_product_quantity(barcode: str, quantity: str, username: str, password: str) -> bool:
    """
    Update product quantity field.
    """
    return update_product_fields(
        barcode,
        {"quantity": quantity},
        username,
        password,
        comment="Automated quantity update via script"
    )

def batch_process(df: pd.DataFrame, operation: str, username: str, password: str) -> Dict[str, int]:
    """
    Batch process all rows updating breeding or quantity info.
    """
    success_count = 0
    failed_count = 0

    print(f"🚀 Starting batch {operation} for {len(df)} products...")

    for idx, row in df.iterrows():
        barcode = str(row['barcode']).strip()
        tag = str(row['tag']).strip()

        print(f"\n[{idx + 1}/{len(df)}] Processing {barcode}...")

        if operation == "breeding":
            success = add_category_to_product(barcode, tag, username, password)
        elif operation == "quantities":
            success = update_product_quantity(barcode, tag, username, password)
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

def get_credentials(args) -> tuple [str, str]:
    """
    Retrieve OFF credentials from args or prompt user.
    """
    username = args.username or os.getenv('OFF_USERNAME')
    password = args.password or os.getenv('OFF_PASSWORD')

    if not username:
        username = input("OpenFoodFacts username: ")
    if not password:
        password = getpass.getpass("OpenFoodFacts password: ")

    return username, password

def parse_args():
    parser = argparse.ArgumentParser(
        description="Update OpenFoodFacts product data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --breeding-types --file breeding.csv
  %(prog)s --quantities --file quantities.csv
  %(prog)s --test-breeding --barcode 3760074380089 --tag "en:organic-eggs"
  %(prog)s --test-quantity --barcode 3760074380089 --tag "12 pcs"
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--breeding-types', action='store_true', help='Update breeding type categories')
    group.add_argument('--quantities', action='store_true', help='Update product quantities')
    group.add_argument('--test-breeding', action='store_true', help='Test breeding type update on single product')
    group.add_argument('--test-quantity', action='store_true', help='Test quantity update on single product')

    parser.add_argument('--file', type=str, help='CSV file path for batch operations')
    parser.add_argument('--barcode', type=str, help='Barcode for test operations')
    parser.add_argument('--tag', type=str, help='Tag/value for test operations')
    parser.add_argument('--username', type=str, help='OpenFoodFacts username (or set OFF_USERNAME env var)')
    parser.add_argument('--password', type=str, help='OpenFoodFacts password (or set OFF_PASSWORD env var)')

    parser.add_argument(
        '--verify-barcodes', dest='verify_barcodes', action='store_true',
        default=True,
        help="Verify that barcodes exist in OpenFoodFacts before processing (default: True)"
    )
    parser.add_argument(
        '--no-verify-barcodes', dest='verify_barcodes', action='store_false',
        help="Disable barcode existence verification (product will be created if barcode does not exist)"
    )

    return parser.parse_args()

def main():
    args = parse_args()

    # Batch operation flow
    if args.breeding_types or args.quantities:
        if not args.file:
            print("❌ Error: --file required for batch operations")
            sys.exit(1)

        csv_path = os.path.join(Config.DATA_DIR, args.file)
        df = load_csv_data(csv_path)
        if df is None:
            sys.exit(1)

        operation = "breeding" if args.breeding_types else "quantities"

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
        if confirm != 'CONFIRM':
            print("Operation cancelled")
            sys.exit(0)

        batch_process(df, operation, username, password)

    # Single test operation flow
    elif args.test_breeding or args.test_quantity:
        if not args.barcode or not args.tag:
            print("❌ Error: --barcode and --tag required for test operations")
            sys.exit(1)

        # Validate tag format before credentials
        if args.test_breeding and not validate_breeding_tag_format(args.tag):
            print(f"❌ Invalid breeding tag '{args.tag}'")
            sys.exit(1)
        if args.test_quantity and not validate_quantity_tag_format(args.tag):
            print(f"❌ Invalid quantity tag '{args.tag}'")
            sys.exit(1)

        username, password = get_credentials(args)

        if not username or not password:
            print("❌ Error: OpenFoodFacts credentials required")
            sys.exit(1)

        if args.test_breeding:
            add_category_to_product(args.barcode, args.tag, username, password)
        else:
            update_product_quantity(args.barcode, args.tag, username, password)

if __name__ == "__main__":
    main()
