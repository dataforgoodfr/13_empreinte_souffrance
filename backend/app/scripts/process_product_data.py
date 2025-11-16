import argparse
import json
from pathlib import Path
from typing import Tuple

import pandas as pd
import plotly.express as px

from app.business.open_food_facts import pain_report_calculator
from app.config.exceptions import ResourceNotFoundException
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalType


# ----------------------------
# Constants
# ----------------------------
class Paths:
    """Paths used in the application."""

    ROOT = Path(__file__).resolve().parents[3]
    ANALYSIS = ROOT / "analysis"
    DATA = Path("data")

    EGGS_CSV = DATA / "eggs_from_parquet.csv"
    POTENTIAL_EGGS_CSV = DATA / "potential_eggs_from_parquet.csv"

    PROCESSED_EGGS = DATA / "processed_products.csv"
    PROCESSED_EGGS_FR = DATA / "processed_products_fr.csv"
    PROCESSED_POTENTIAL_EGGS = DATA / "processed_potential_eggs.csv"

    COLS_TO_JSON = DATA / "cols_to_json.txt"
    OCR_JSONL_FILE = (
        ANALYSIS / "neural_category_predictions/data/dfoeufs_with_predictions_with_ground_truth_with_groq_spans.jsonl"
    )


class Config:
    """Application-wide configuration constants."""

    FRENCH_TAG = "en:france"
    OCR_LINE_SEPARATOR = " . "
    SUNBURST_WIDTH = 500
    SUNBURST_HEIGHT = 500
    SUNBURST_MARGIN = dict(t=40, l=10, r=10, b=10)
    SUNBURST_TEXT_SIZE = 12


class EggConsts:
    """Constants representing special cases for egg metrics."""

    COUNT_NOT_COMPUTED = -1
    COUNT_NOT_MANAGED = -2
    CALIBER_NOT_COMPUTED = "no caliber"
    CALIBER_NOT_MANAGED = "not managed"
    BREEDING_NOT_COMPUTED = "no breeding"
    BREEDING_NOT_MANAGED = "not managed"


class OcrKeys:
    """Structure description for OCR JSONL file with nested keys."""

    ROOT_KEYS = ["code", "ocr_text"]
    NESTED_KEYS = {
        "groq_spans": ["breeding_type_related", "weight_related"],
        "lewagon_prediction": ["proba_1", "proba_2", "proba_3"],
    }


# ----------------------------
# Utility functions
# ----------------------------
def safe_json_loads(s):
    """Safely parse a JSON string."""
    if isinstance(s, str):
        s_strip = s.strip()
        if s_strip.startswith(("[", "{")):
            try:
                return json.loads(s_strip)
            except json.JSONDecodeError:
                pass
    return s


def parse_json_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Parse all columns in the DataFrame that contain JSON strings."""
    with open(Paths.COLS_TO_JSON, "r") as f:
        cols_to_json = json.load(f)
    for col in cols_to_json:
        if col in df.columns:
            df[col] = df[col].apply(safe_json_loads)
    return df


def extract_text(row_dict: dict, field: str) -> str:
    """Extract 'text' from a nested list of dicts."""
    val = row_dict.get(field)
    if isinstance(val, list) and val and isinstance(val[0], dict) and "text" in val[0]:
        return val[0]["text"]
    return ""


def row_to_product_data(row) -> ProductData:
    """Convert a DataFrame row to ProductData."""
    normalized_row = {
        k: v if isinstance(v, (list, dict)) else (None if pd.isna(v) else v) for k, v in row.to_dict().items()
    }
    normalized_row["product_name"] = extract_text(normalized_row, "product_name")
    normalized_row["generic_name"] = extract_text(normalized_row, "generic_name")
    normalized_row["ingredients"] = normalized_row.get("ingredients")
    try:
        return ProductData.model_validate(normalized_row)
    except Exception as e:
        print(f"Error processing product {row.get('code', 'unknown')}: {e}")
        return ProductData.model_validate(normalized_row, strict=False)


def load_eggs_df(input_file: Path) -> pd.DataFrame:
    """Load eggs CSV and parse JSON columns."""
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error loading eggs from {input_file}: {e}")
        exit(1)

    return parse_json_columns(df)


def create_dataframe_from_jsonl(file_path: Path) -> pd.DataFrame:
    """Convert OCR JSONL file to DataFrame using nested keys."""
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
                record = {key: rec.get(key) for key in OcrKeys.ROOT_KEYS}
                for parent_key, child_keys in OcrKeys.NESTED_KEYS.items():
                    nested = rec.get(parent_key) or {}
                    for child in child_keys:
                        record[child] = nested.get(child)
                records.append(record)
            except json.JSONDecodeError:
                print(f"JSON error line {line_num}, ignored - code {rec.get('code')}")
            except Exception as e:
                print(f"Unexpected error line {line_num}: {e}")
    return pd.DataFrame(records)


def enrich_eggs_with_ocr(eggs_df: pd.DataFrame, ocr_df: pd.DataFrame) -> pd.DataFrame:
    """Merge eggs DataFrame with OCR predictions and clean OCR text."""
    merged = eggs_df.merge(ocr_df, on="code", how="left")
    merged["ocr_text"] = (
        merged["ocr_text"].str.replace(r"\n|\r\n|\r", Config.OCR_LINE_SEPARATOR, regex=True).str.lower()
    )
    return merged


def row_to_breeding_type_and_quantity(row) -> Tuple[int, str, str]:
    """Compute breeding type and egg quantity for a row."""
    try:
        product_data = row_to_product_data(row)
        report = pain_report_calculator.PainReportCalculator(product_data)
        quantities = report._get_quantities()
        breeding_types = report._get_breeding_types()
    except ResourceNotFoundException:
        return (EggConsts.COUNT_NOT_MANAGED, EggConsts.CALIBER_NOT_MANAGED, EggConsts.BREEDING_NOT_MANAGED)

    quantity = quantities.get(AnimalType.LAYING_HEN)
    if not quantity:
        egg_count = EggConsts.COUNT_NOT_COMPUTED
        caliber = EggConsts.CALIBER_NOT_COMPUTED
    else:
        egg_count = quantity.count
        caliber = quantity.caliber or EggConsts.CALIBER_NOT_COMPUTED

    breeding_type = breeding_types.get(AnimalType.LAYING_HEN)
    if not breeding_type:
        breeding = EggConsts.BREEDING_NOT_COMPUTED
    elif isinstance(breeding_type, str):
        breeding = breeding_type
    else:
        breeding = breeding_type.breeding_type.value

    return egg_count, caliber, breeding


def prepare_egg_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add display-friendly columns to DataFrame."""
    df = df.copy()
    df["egg_count_string"] = df["egg_count"].apply(
        lambda egg_count: "no count"
        if egg_count == EggConsts.COUNT_NOT_COMPUTED
        else "not managed"
        if egg_count == EggConsts.COUNT_NOT_MANAGED
        else "count found"
    )
    df["french_string"] = df["french"].apply(lambda x: "french" if x else "not french")
    return df


# ----------------------------
# Pipeline functions
# ----------------------------
def enrich_with_ocr_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich eggs DataFrame with OCR data."""
    ocr_df = create_dataframe_from_jsonl(Paths.OCR_JSONL_FILE)
    return enrich_eggs_with_ocr(df, ocr_df)


def compute_egg_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute egg count, caliber and breeding columns."""
    df[["egg_count", "caliber", "breeding"]] = df.apply(
        lambda row: pd.Series(row_to_breeding_type_and_quantity(row)), axis=1
    )
    return df


def add_french_column_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Add 'french' boolean column if not present."""
    if "french" not in df.columns:
        df["french"] = (
            df.get("countries_tags", pd.Series())
            .fillna("")
            .apply(lambda x: Config.FRENCH_TAG in x if len(x) > 0 else False)
        )
    return df


def save_processed_data(df: pd.DataFrame, dataset: str) -> None:
    """Save processed DataFrame to CSV and French subset if applicable."""
    processed_file, _ = get_file_paths(dataset)
    df.to_csv(processed_file, index=False)
    print(f"Saved processed data to {processed_file}")
    if dataset != "potential":
        df[df["french"]].to_csv(Paths.PROCESSED_EGGS_FR, index=False)
        print(f"Saved French subset to {Paths.PROCESSED_EGGS_FR}")


def full_processing_pipeline(input_file: Path, dataset: str) -> pd.DataFrame:
    """Full processing pipeline: load, enrich, compute metrics, and save."""
    df = load_eggs_df(input_file)
    if dataset != "potential":
        df = enrich_with_ocr_pipeline(df)
    df = compute_egg_metrics(df)
    df = prepare_egg_display_columns(add_french_column_pipeline(df))
    save_processed_data(df, dataset)
    return df


# ----------------------------
# Chart functions
# ----------------------------
def plot_egg_sunburst(df: pd.DataFrame, dataset: str, include_caliber: bool) -> None:
    """Plot a sunburst chart to visualize egg metrics."""
    if dataset == "world":
        data = df
        title_prefix = "All eggs (World)"
        path = [px.Constant("all"), "french_string", "breeding", "egg_count_string"]
    elif dataset == "france":
        data = df[df["french"]].copy()
        title_prefix = "French eggs"
        path = [px.Constant("all"), "breeding", "egg_count_string"]
    else:
        raise ValueError("dataset must be one of ['world', 'france']")

    if include_caliber:
        path.append("caliber")

    fig = px.sunburst(data, path=path)
    fig.update_traces(
        texttemplate="%{label}<br>%{percentRoot:.1%}<br>%{value}",
        textfont=dict(size=Config.SUNBURST_TEXT_SIZE),
        insidetextorientation="horizontal",
    )
    fig.update_layout(
        title=f"{title_prefix} : {'with' if include_caliber else 'without'} caliber",
        width=Config.SUNBURST_WIDTH,
        height=Config.SUNBURST_HEIGHT,
        margin=Config.SUNBURST_MARGIN,
    )
    fig.show()


def manage_chart_display(df: pd.DataFrame, dataset: str, include_caliber: bool, no_plot: bool) -> None:
    """Display sunburst chart or skip depending on arguments."""
    if not no_plot and dataset != "potential":
        plot_egg_sunburst(df, dataset, include_caliber)
        print(f"Sunburst chart displayed for {dataset}, caliber {'included' if include_caliber else 'excluded'}")
    elif dataset == "potential":
        print(f"No coverage chart for potential eggs - {df.shape[0]} products")
    else:
        print("Chart display disabled")


# ----------------------------
# Command line & main
# ----------------------------
def get_file_paths(dataset: str) -> tuple[Path, Path]:
    """Return processed file and input CSV paths based on dataset."""
    if dataset == "world":
        return Paths.PROCESSED_EGGS, Paths.EGGS_CSV
    elif dataset == "france":
        return Paths.PROCESSED_EGGS_FR, Paths.EGGS_CSV
    elif dataset == "potential":
        return Paths.PROCESSED_POTENTIAL_EGGS, Paths.POTENTIAL_EGGS_CSV
    else:
        raise ValueError(f"Unknown dataset: {dataset}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process egg product data with OCR predictions and calculate breeding types"
    )
    parser.add_argument("--dataset", choices=["world", "france", "potential"], default="france", required=True)
    parser.add_argument("--include-caliber", action="store_true")
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--no-process", action="store_true")
    return parser.parse_args()


def load_processed_data(processed_file: Path) -> pd.DataFrame:
    """Load already processed CSV and parse JSON columns."""
    if not processed_file.exists():
        raise FileNotFoundError(f"Processed file {processed_file} not found. Run without --no-process first.")
    df = pd.read_csv(processed_file)
    df = parse_json_columns(df)
    print(f"Loaded processed data with {len(df)} rows from {processed_file}")
    return df


def main():
    """Main execution function."""
    args = parse_arguments()
    processed_file, input_file = get_file_paths(args.dataset)
    df = load_processed_data(processed_file) if args.no_process else full_processing_pipeline(input_file, args.dataset)
    manage_chart_display(df, args.dataset, args.include_caliber, args.no_plot)


if __name__ == "__main__":
    main()
