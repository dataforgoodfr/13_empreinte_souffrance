#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Excel Product Data Exporter

This module provides functionality to export product data from a pandas DataFrame
to formatted Excel files with images, product information, and analysis results.
The script is specifically designed for egg product analysis including breeding
type, quantity, and OCR text extraction.

Author: Data Analysis Team
Date: 2025
"""

import argparse
import json
import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from tqdm import tqdm

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# File paths
DATA_PATH = "C:\\dev\\git\\13_empreinte_souffrance\\backend\\app\\scripts\\data\\"
INPUT_CSV_FILE = "processed_products.csv"
OUTPUT_EXCEL_FILE = "products_to_tag_14_06_25.xlsx"
ALL_PRODUCTS_EXCEL_FILE = "all_products.xlsx"
TEST_EXCEL_FILE = "products_test.xlsx"

# Excel configuration
DEFAULT_SHEET_NAME = "Feuille1"
EXCEL_EXTENSION = ".xlsx"
IMAGE_COUNT = 10
ROW_HEIGHT = 300
HEADER_FONT_SIZE = 8
TEST_SAMPLE_SIZE = 10

# OpenFoodFacts URLs
PRODUCT_BASE_URL = "https://fr.openfoodfacts.org/produit/"
IMAGE_BASE_URL = "https://images.openfoodfacts.net/images/products/"

# Column definitions
BASE_COLUMNS = ["Traité", "Info invisible", "Pas œuf", "Code et URL produit", "Autres", "Catégories", "Quantité"]

OPTIONAL_COLUMNS = {"breeding": ["Elevage"], "quantity": ["Qté", "Calibre"]}

NEW_ANALYSIS_COLUMNS = ["OCR", "breeding_type_related", "weight_type_related", "predictions_categories"]

COLUMN_RENAMES = {
    "Traité": "Traité",
    "Info invisible": "Info invisible",
    "Pas œuf": "Pas œuf / comment.",
    "Code et URL produit": "Code et URL produit",
    "Image front": "Image principale",
    "Image ingredients": "Image ingrédients",
    "Autres": "Nom, ingrédients, labels",
    "Catégories": "Catégories",
    "Quantité": "Quantité",
    "Elevage": "Elevage\n (cage, sol, plein-air, bio ou 3, 2, 1, 0)",
    "Qté": "Quantité\n(nb d'œufs ou poids)",
    "Calibre": "Calibre\n(S, M, L, XL ou petit, moyen, gros, très gros)",
    "OCR": "OCR",
    "breeding_type_related": "breeding_type_related",
    "weight_type_related": "weight_type_related",
    "predictions_categories": "predictions categories",
}

# Column width settings for Excel formatting
COLUMN_WIDTHS = {
    "Traité": 8,
    "Info invisible": 10,
    "Pas œuf / comment.": 10,
    "Code et URL produit": 15,
    "Nom, ingrédients, labels": 22,
    "Catégories": 22,
    "Quantité": 15,
    "Image principale": 50,
    "Image ingrédients": 50,
    "Elevage\n (cage, sol, plein-air, bio ou 3, 2, 1, 0)": 15,
    "Quantité\n(nb d'œufs ou poids)": 13,
    "Calibre\n(S, M, L, XL ou petit, moyen, gros, très gros)": 17,
    "OCR": 50,
    "breeding_type_related": 15,
    "weight_type_related": 15,
    "predictions categories": 15,
    **{f"Image {i}": 50 for i in range(1, IMAGE_COUNT + 1)},
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def load_product_data(file_path: str) -> pd.DataFrame:
    """
    Load product data from CSV file.

    Args:
        file_path: Path to the CSV file containing product data

    Returns:
        DataFrame containing the product data

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        pd.errors.EmptyDataError: If the CSV file is empty
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
        print(f"✅ Loaded {len(df)} products from {file_path}")
        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError(f"The file {file_path} is empty")


def get_product_code_lists(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Generate lists of product codes based on missing breeding/quantity information.

    Args:
        df: DataFrame containing product data with 'breeding' and 'egg_count' columns

    Returns:
        Dictionary containing different categories of product codes:
        - no_breeding_no_quantity: Products missing both breeding type and quantity
        - no_breeding: Products missing only breeding type
        - no_quantity_not_free_range: Non-free-range products missing quantity
        - no_quantity: Products with breeding type but missing quantity
    """
    # Products with no breeding type and no quantity
    no_breeding_no_quantity = df.loc[
        (df["breeding"].isin(["not managed", "no breeding"])) & (df["egg_count"] < 0), "code"
    ].tolist()

    # Products with no breeding type but with quantity
    no_breeding = df.loc[
        (df["breeding"].isin(["not managed", "no breeding"])) & (df["egg_count"] >= 0), "code"
    ].tolist()

    # Products with breeding type (not free range) but no quantity
    no_quantity_not_free_range = df.loc[
        (df["breeding"] != "free_range")
        & (df["breeding"] != "not managed")
        & (df["breeding"] != "no breeding")
        & (df["egg_count"] < 0),
        "code",
    ].tolist()

    # Products with breeding type but no quantity
    no_quantity = df.loc[
        (df["breeding"] != "not managed") & (df["breeding"] != "no breeding") & (df["egg_count"] == 0), "code"
    ].tolist()

    return {
        "no_breeding_no_quantity": no_breeding_no_quantity,
        "no_breeding": no_breeding,
        "no_quantity_not_free_range": no_quantity_not_free_range,
        "no_quantity": no_quantity,
    }


def get_random_sample_codes(df: pd.DataFrame, sample_size: int = TEST_SAMPLE_SIZE) -> List[str]:
    """
    Get random sample of product codes for testing.

    Args:
        df: DataFrame containing product data
        sample_size: Number of products to sample

    Returns:
        List of randomly selected product codes
    """
    if len(df) < sample_size:
        sample_size = len(df)

    sample_df = df.sample(n=sample_size)
    return sample_df["code"].tolist()


# =============================================================================
# MAIN EXCEL GENERATOR CLASS
# =============================================================================


class ExcelProductGenerator:
    """
    Handles generation of formatted Excel files from product DataFrame data.

    This class processes product information including images, breeding data,
    quantity information, and OCR results to create comprehensive Excel reports
    for manual data validation and completion.
    """

    def __init__(self, data_path: str = DATA_PATH):
        """
        Initialize the Excel generator.

        Args:
            data_path: Base directory path for input/output files
        """
        self.data_path = data_path

    def build_product_row(
        self, product: Dict, code: str, df: pd.DataFrame, show_breeding: bool, show_quantity: bool
    ) -> Dict:
        """
        Build a complete Excel row from product data.

        Args:
            product: Dictionary containing product information from DataFrame
            code: Product barcode/identifier
            df: Source DataFrame for additional data lookup
            show_breeding: Whether to include breeding information column
            show_quantity: Whether to include quantity information columns

        Returns:
            Dictionary representing a complete row for Excel export
        """
        # Extract and parse product information
        product_name = self._parse_multilingual_field(product.get("product_name", []))
        generic_name = self._parse_multilingual_field(product.get("generic_name", ""))

        ingredients = product.get("ingredients_tags", [])
        labels = product.get("labels_tags", [])
        categories = product.get("categories_tags", [])

        # Get quantity from DataFrame
        quantity_value = self._get_dataframe_value(code, df, "quantity") or ""

        # Get breeding and egg_count from DataFrame
        breeding_value = self._get_dataframe_value(code, df, "breeding") or ""
        egg_count_value = self._get_dataframe_value(code, df, "egg_count") or ""

        # Build image URLs
        image_urls = self._build_image_urls(code, product.get("images", []))

        # Create base row structure
        row = {
            "Traité": "",
            "Info invisible": "",
            "Pas œuf": "",
            "Code et URL produit": code,
            "Autres": f"{product_name}\n{generic_name}\n{ingredients}\n{labels}",
            "Catégories": str(categories),
            "Quantité": quantity_value,
        }

        # Add image columns
        for i in range(IMAGE_COUNT):
            if i < len(image_urls):
                row[f"Image {i + 1}"] = f'=IMAGE("{image_urls[i]}")'
            else:
                row[f"Image {i + 1}"] = ""

        # Add optional columns based on configuration
        if show_breeding:
            row["Elevage"] = breeding_value

        if show_quantity:
            row["Qté"] = egg_count_value
            row["Calibre"] = ""

        # Add analysis columns (OCR, predictions, etc.)
        analysis_data = self._get_analysis_data(code, df)
        row.update(analysis_data)

        return row

    def _parse_multilingual_field(self, field_data) -> str:
        """
        Parse multilingual field data from OpenFoodFacts format.

        Args:
            field_data: Raw field data (string, list, or dict)

        Returns:
            Formatted string with newline-separated values
        """
        if isinstance(field_data, str):
            try:
                parsed_data = json.loads(field_data.replace("'", '"').replace("None", "null"))
            except json.JSONDecodeError:
                return str(field_data)
        else:
            parsed_data = field_data

        if isinstance(parsed_data, list):
            return "\n".join(d.get("text", "") for d in parsed_data if isinstance(d, dict) and d.get("lang") != "main")
        else:
            return str(parsed_data) if parsed_data else ""

    def _build_image_urls(self, code: str, images_raw) -> List[str]:
        """
        Build image URLs from product code and image data.

        Args:
            code: Product barcode
            images_raw: Raw image data from product information

        Returns:
            List of formatted image URLs
        """
        # Parse images data
        if isinstance(images_raw, str):
            try:
                images_list = json.loads(images_raw.replace("'", '"').replace("None", "null"))
            except json.JSONDecodeError:
                images_list = []
        else:
            images_list = images_raw if images_raw else []

        # Build URL path from padded code
        code_padded = str(code).zfill(13)
        path = f"{code_padded[:3]}/{code_padded[3:6]}/{code_padded[6:9]}/{code_padded[9:]}"

        # Extract and sort image keys
        image_keys = sorted(
            [img["key"] for img in images_list if isinstance(img, dict) and str(img.get("key")).isdigit()], key=int
        )

        # Build complete URLs
        return [f"{IMAGE_BASE_URL}{path}/{k}.jpg" for k in image_keys][:IMAGE_COUNT]

    def _get_analysis_data(self, code: str, df: pd.DataFrame) -> Dict[str, str]:
        """
        Get analysis data (OCR, predictions, etc.) for a product.

        Args:
            code: Product barcode
            df: Source DataFrame

        Returns:
            Dictionary with analysis data fields
        """
        analysis_data = {}

        # OCR text
        analysis_data["OCR"] = self._get_dataframe_value(code, df, "texte_ocr") or ""

        # Breeding and weight type related data
        analysis_data["breeding_type_related"] = self._get_dataframe_value(code, df, "breeding_type_related") or ""
        analysis_data["weight_type_related"] = self._get_dataframe_value(code, df, "weight_type_related") or ""

        # Prediction categories (concatenate proba_1, proba_2, proba_3)
        proba_values = []
        for col in ["proba_1", "proba_2", "proba_3"]:
            value = self._get_dataframe_value(code, df, col)
            if value:
                proba_values.append(value)

        analysis_data["predictions_categories"] = "\n".join(proba_values)

        return analysis_data

    def _get_dataframe_value(self, code: str, df: pd.DataFrame, column: str) -> Optional[str]:
        """
        Get a specific value from DataFrame for a product code.

        Args:
            code: Product barcode
            df: Source DataFrame
            column: Column name to retrieve

        Returns:
            String value or None if not found/empty
        """
        try:
            mask = df["code"] == code
            if mask.any():
                value = df.loc[mask, column].iloc[0]
                return str(value) if pd.notna(value) else None
        except (KeyError, IndexError):
            pass
        return None

    def _fetch_product_data(self, code: str, df: pd.DataFrame) -> Optional[Dict]:
        """
        Fetch complete product data from DataFrame.

        Args:
            code: Product barcode
            df: Source DataFrame

        Returns:
            Dictionary with product data or empty dict if not found
        """
        row = df[df["code"] == code]
        if not row.empty:
            return row.iloc[0].replace({np.nan: None}).to_dict()
        return {}

    def _create_column_order(self, show_breeding: bool, show_quantity: bool) -> List[str]:
        """
        Create the proper column order for Excel output.

        Args:
            show_breeding: Whether to include breeding column
            show_quantity: Whether to include quantity columns

        Returns:
            List of column names in proper order
        """
        columns = ["Traité"]

        if show_breeding:
            columns.extend(OPTIONAL_COLUMNS["breeding"])

        if show_quantity:
            columns.extend(OPTIONAL_COLUMNS["quantity"])

        columns.extend(BASE_COLUMNS[1:])  # Skip "Traité" as it's already added
        columns.extend(NEW_ANALYSIS_COLUMNS)  # Add analysis columns
        columns.extend([f"Image {i + 1}" for i in range(IMAGE_COUNT)])  # Add image columns

        return columns

    def format_excel_file(
        self,
        filename: str,
        columns: List[str],
        product_codes: List[str],
        sheet_name: str = DEFAULT_SHEET_NAME,
        show_progress: bool = True,
    ) -> None:
        """
        Apply formatting to the Excel file including styles, hyperlinks, and layout.

        Args:
            filename: Path to the Excel file
            columns: List of column names
            product_codes: List of product codes for hyperlink generation
            sheet_name: Name of the sheet to format
            show_progress: Whether to show a progress bar
        """
        wb = load_workbook(filename)
        ws = wb[sheet_name]

        # Ajout des hyperliens
        code_col_idx = columns.index("Code et URL produit") + 1
        hyperlink_iter = product_codes
        if show_progress:
            hyperlink_iter = tqdm(product_codes, desc="Adding hyperlinks", unit="code")

        for i, code in enumerate(hyperlink_iter):
            cell = ws.cell(row=i + 2, column=code_col_idx)
            cell.hyperlink = f"{PRODUCT_BASE_URL}{code}"
            cell.style = "Hyperlink"

        # Largeur des colonnes
        if show_progress:
            tqdm.write("Adjusting column widths...")
        for idx, name in enumerate(columns, 1):
            ws.column_dimensions[get_column_letter(idx)].width = COLUMN_WIDTHS.get(name, 15)

        # Hauteur des lignes pour images
        if show_progress:
            tqdm.write("Setting row heights...")
        for r in range(2, 2 + len(product_codes)):
            ws.row_dimensions[r].height = ROW_HEIGHT

        # Définition des styles
        fill_gray = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        border = Border(
            left=Side(style="dotted", color="E0E0E0"),
            right=Side(style="dotted", color="E0E0E0"),
            top=Side(style="thin", color="AAAAAA"),
            bottom=Side(style="thin", color="AAAAAA"),
        )

        # Application de la mise en forme des cellules
        all_rows = list(ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column))
        cell_iter = all_rows
        if show_progress:
            cell_iter = tqdm(all_rows, desc="Applying cell formatting", unit="row")

        for row in cell_iter:
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
                cell.border = border

        # Ligne d’en-tête
        for cell in ws[1]:
            cell.alignment = Alignment(horizontal="center", wrap_text=True, vertical="center")
            cell.font = Font(size=HEADER_FONT_SIZE, bold=True)

        # Gel des volets + couleur grise
        if "Pas œuf / comment." in columns:
            freeze_col_idx = columns.index("Pas œuf / comment.") + 2
            ws.freeze_panes = ws.cell(row=2, column=freeze_col_idx)

            for r in range(2, ws.max_row + 1):
                for c in range(freeze_col_idx, ws.max_column + 1):
                    ws.cell(row=r, column=c).fill = fill_gray

        wb.save(filename)
        if show_progress:
            tqdm.write(f"✅ Excel sheet '{sheet_name}' generated in {filename}")

    def generate_excel(
        self,
        product_codes: List[str],
        df: pd.DataFrame,
        output_filename: str,
        show_col_breeding: bool = True,
        show_cols_quantity: bool = True,
        sheet_name: str = DEFAULT_SHEET_NAME,
        show_progress: bool = True,
    ) -> str:
        if not output_filename.endswith(EXCEL_EXTENSION):
            output_filename += EXCEL_EXTENSION
        file_path = os.path.join(self.data_path, output_filename)

        total_products = len(product_codes)

        rows = []
        valid_codes = []
        processed_count = 0
        failed_count = 0

        # Barre de progression
        iterable = product_codes
        if show_progress:
            iterable = tqdm(product_codes, desc=f"Processing {total_products} products", unit="product")

        for code in iterable:
            try:
                product = self._fetch_product_data(code, df)
                if product:
                    row = self.build_product_row(product, code, df, show_col_breeding, show_cols_quantity)
                    rows.append(row)
                    valid_codes.append(code)
                    processed_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1
                continue

        if not rows:
            raise ValueError("No valid products found to process")

        # Info finale si show_progress
        if show_progress:
            tqdm.write(f"✅ Successfully processed: {processed_count} | ❌ Failed: {failed_count}")

        column_order = self._create_column_order(show_col_breeding, show_cols_quantity)
        df_output = pd.DataFrame(rows)
        df_output = df_output.reindex(columns=column_order)
        df_output.rename(columns=COLUMN_RENAMES, inplace=True)

        self._write_to_excel(df_output, file_path, sheet_name)
        self.format_excel_file(file_path, df_output.columns.tolist(), valid_codes, sheet_name)

        return file_path

    def _write_to_excel(self, df_output: pd.DataFrame, file_path: str, sheet_name: str) -> None:
        """
        Write DataFrame to Excel file, handling existing files appropriately.

        Args:
            df_output: Formatted DataFrame to write
            file_path: Full path to the Excel file
            sheet_name: Name of the sheet to create/replace
        """
        # Handle existing file
        if os.path.exists(file_path):
            wb = load_workbook(file_path)
            if sheet_name in wb.sheetnames:
                del wb[sheet_name]
            ws = wb.create_sheet(title=sheet_name)
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = sheet_name

        # Write headers
        for col_idx, col_name in enumerate(df_output.columns, start=1):
            ws.cell(row=1, column=col_idx, value=col_name)

        # Write data rows
        for row_idx, row_data in enumerate(df_output.itertuples(index=False), start=2):
            for col_idx, cell_value in enumerate(row_data, start=1):
                ws.cell(row=row_idx, column=col_idx, value=cell_value)

        wb.save(file_path)


# =============================================================================
# MAIN EXECUTION FUNCTIONS
# =============================================================================


def create_test_excel(df: pd.DataFrame, generator: ExcelProductGenerator) -> None:
    """
    Create a test Excel file with random sample products.

    Args:
        df: Source DataFrame containing product data
        generator: ExcelProductGenerator instance
    """
    print("Creating test Excel with random products...")
    sample_codes = get_random_sample_codes(df, TEST_SAMPLE_SIZE)
    print(f"Selected products: {sample_codes}")

    generator.generate_excel(
        product_codes=sample_codes,
        df=df,
        output_filename=TEST_EXCEL_FILE,
        show_col_breeding=True,
        show_cols_quantity=True,
        sheet_name="Test products",
        show_progress=False,  # No progress for test mode
    )

    # Open file (Windows only)
    if os.name == "nt":
        os.startfile(os.path.join(generator.data_path, TEST_EXCEL_FILE))


def create_all_products_excel(df: pd.DataFrame, generator: ExcelProductGenerator) -> None:
    """
    Create Excel file with all products without filters.

    Args:
        df: Source DataFrame containing product data
        generator: ExcelProductGenerator instance
    """
    print("Creating Excel with all products...")
    all_codes = df["code"].tolist()
    print(f"Total number of products: {len(all_codes)}")

    generator.generate_excel(
        product_codes=all_codes,
        df=df,
        output_filename=ALL_PRODUCTS_EXCEL_FILE,
        show_col_breeding=True,
        show_cols_quantity=True,
        sheet_name="All products",
        show_progress=True,  # Show progress for large datasets
    )

    # Open file (Windows only)
    if os.name == "nt":
        os.startfile(os.path.join(generator.data_path, ALL_PRODUCTS_EXCEL_FILE))


def create_production_excel(df: pd.DataFrame, generator: ExcelProductGenerator) -> None:
    """
    Create production Excel file with all product categories.

    Args:
        df: Source DataFrame containing product data
        generator: ExcelProductGenerator instance
    """
    print("Creating production Excel for all product categories...")
    print("=" * 60)

    # Get product code lists
    code_lists = get_product_code_lists(df)

    print("📋 Category breakdown:")
    print(f"  • No breeding & no quantity: {len(code_lists['no_breeding_no_quantity'])} products")
    print(f"  • No breeding only: {len(code_lists['no_breeding'])} products")
    print(f"  • Non-free-range with no quantity: {len(code_lists['no_quantity_not_free_range'])} products")
    print()

    total_sheets = 3
    current_sheet = 0

    # Generate sheets for different product categories
    current_sheet += 1
    print(f"🔄 [{current_sheet}/{total_sheets}] Processing 'no_breeding_no_quantity' sheet...")
    generator.generate_excel(
        product_codes=code_lists["no_breeding_no_quantity"],
        df=df,
        output_filename=OUTPUT_EXCEL_FILE,
        show_col_breeding=True,
        show_cols_quantity=True,
        sheet_name="no_breeding_no_quantity",
        show_progress=True,
    )
    print()

    current_sheet += 1
    print(f"🔄 [{current_sheet}/{total_sheets}] Processing 'no_breeding' sheet...")
    generator.generate_excel(
        product_codes=code_lists["no_breeding"],
        df=df,
        output_filename=OUTPUT_EXCEL_FILE,
        show_col_breeding=True,
        show_cols_quantity=True,
        sheet_name="no_breeding",
        show_progress=True,
    )
    print()

    current_sheet += 1
    print(f"🔄 [{current_sheet}/{total_sheets}] Processing 'no_quantity_not_free_range' sheet...")
    generator.generate_excel(
        product_codes=code_lists["no_quantity_not_free_range"],
        df=df,
        output_filename=OUTPUT_EXCEL_FILE,
        show_col_breeding=True,
        show_cols_quantity=True,
        sheet_name="no_quantity_not_free_range",
        show_progress=True,
    )

    print("=" * 60)
    print(f"🎉 All {total_sheets} sheets completed successfully!")

    # Open file (Windows only)
    if os.name == "nt":
        os.startfile(os.path.join(generator.data_path, OUTPUT_EXCEL_FILE))


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Namespace containing parsed arguments
    """
    parser = argparse.ArgumentParser(description="Export product data to Excel with filtering options")

    parser.add_argument(
        "--test", action="store_true", help=f"Create test Excel with {TEST_SAMPLE_SIZE} random products"
    )

    parser.add_argument("--all-products", action="store_true", help="Create Excel with all products without filters")

    parser.add_argument("--production", action="store_true", help="Create production Excel with filtered categories")

    return parser.parse_args()


def main():
    """
    Main execution function with command line argument handling.
    """
    try:
        # Parse arguments
        args = parse_arguments()

        # Load data
        input_file_path = os.path.join(DATA_PATH, INPUT_CSV_FILE)
        df = load_product_data(input_file_path)

        # Initialize generator
        generator = ExcelProductGenerator(DATA_PATH)

        # Handle command line options
        if args.test:
            create_test_excel(df, generator)
        elif args.all_products:
            create_all_products_excel(df, generator)
        elif args.production:
            create_production_excel(df, generator)
        else:
            # Interactive mode if no arguments provided
            print("Interactive mode - Choose an option:")
            print("1. Test Excel (random products)")
            print("2. Excel with all products")
            print("3. Production Excel (filtered categories)")

            choice = input("Your choice (1/2/3): ")

            if choice == "1":
                create_test_excel(df, generator)
            elif choice == "2":
                create_all_products_excel(df, generator)
            elif choice == "3":
                create_production_excel(df, generator)
            else:
                print("Invalid choice, stopping program")
                return

        print("\n✅ Script execution completed successfully!")

    except Exception as e:
        print(f"❌ Error during execution: {e}")
        raise


if __name__ == "__main__":
    main()
