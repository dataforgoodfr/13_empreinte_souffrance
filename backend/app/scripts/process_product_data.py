import argparse
import json
from pathlib import Path

import pandas as pd
import plotly.express as px

from app.business.open_food_facts import pain_report_calculator
from app.config.exceptions import ResourceNotFoundException
from app.schemas.open_food_facts.external import ProductData

ROOT_PATH = Path(__file__).resolve().parents[3]
ANALYSIS_PATH = ROOT_PATH / "analysis"
DATA_PATH = Path("data")

JSONL_FILE_PATH = (
    ANALYSIS_PATH
    / "neural_category_predictions"
    / "data"
    / "dfoeufs_with_predictions_with_ground_truth_with_groq_spans.jsonl"
)
EGGS_CSV_PATH = DATA_PATH / "eggs_from_parquet.csv"
COLS_TO_JSON_PATH = DATA_PATH / "cols_to_json.txt"


def safe_json_loads(s):
    """
    Safely loads Json strings as saved in the OFF dataset.

    Args:
        s (str): Input string potentially containing JSON.

    Returns:
        object: Parsed JSON object or original input.
    """
    if isinstance(s, str):
        s_strip = s.strip()
        if s_strip.startswith(("[", "{")):
            try:
                return json.loads(s_strip)
            except json.JSONDecodeError:
                pass
    return s


def load_eggs_df() -> pd.DataFrame:
    """
    Loads the eggs DataFrame from CSV and converts specified columns from JSON strings to Python objects.

    Returns:
        pd.DataFrame: DataFrame containing eggs data with JSON columns parsed.
    """
    df = pd.read_csv(EGGS_CSV_PATH)
    with open(COLS_TO_JSON_PATH, "r") as f:
        cols_to_json = json.load(f)
    for col in cols_to_json:
        df[col] = df[col].apply(safe_json_loads)
    return df


def create_dataframe_from_jsonl(file_path: Path) -> pd.DataFrame:
    """
    Converts the JSONL file containing OCR predictions into a DataFrame

    Args:
        file_path (Path): Path to the JSONL file.

    Returns:
        pd.DataFrame: DataFrame containing extracted data from JSONL lines.
    """
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                rec = json.loads(line)
                groq_spans = rec.get("groq_spans") or {}
                lewagon_pred = rec.get("lewagon_prediction") or {}

                records.append(
                    {
                        "code": rec.get("code"),
                        "texte_ocr": rec.get("ocr_text"),
                        "breeding_type_related": groq_spans.get("breeding_type_related"),
                        "weight_related": groq_spans.get("weight_related"),
                        "proba_1": lewagon_pred.get("proba_1"),
                        "proba_2": lewagon_pred.get("proba_2"),
                        "proba_3": lewagon_pred.get("proba_3"),
                    }
                )
            except json.JSONDecodeError:
                print(f"Erreur JSON à la ligne {line_num}, ignorée - code {rec.get('code')}.")
            except Exception as e:
                print(f"Erreur inattendue à la ligne {line_num} : {e}")
    return pd.DataFrame(records)


def enrich_eggs_with_ocr(eggs_df: pd.DataFrame, ocr_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge eggs DataFrame with OCR predictions and clean OCR text.

    Args:
        eggs_df (pd.DataFrame): Eggs DataFrame.
        ocr_df (pd.DataFrame): OCR data DataFrame.

    Returns:
        pd.DataFrame: Merged DataFrame with cleaned OCR text.
    """
    merged = eggs_df.merge(ocr_df, on="code", how="left")
    merged["texte_ocr"] = merged["texte_ocr"].str.replace(r"\n|\r\n|\r", " . ", regex=True).str.lower()
    return merged


def row_to_product_data(row) -> ProductData:
    """
    Converts a product row into a validated ProductData instance.

    The function cleans values by converting NaNs to None and extracts
    'product_name' and 'generic_name' from nested structures.

    Args:
        row (pd.Series): Single row from a DataFrame.

    Returns:
        ProductData: Validated product data object.
    """

    def extract_text_field(field):
        val = drow.get(field)
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict) and "text" in val[0]:
            return val[0]["text"]
        return ""

    drow = {k: v if isinstance(v, (list, dict)) else (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

    try:
        drow["ingredients"] = drow.get("ingredients")
        drow["product_name"] = extract_text_field("product_name")
        drow["generic_name"] = extract_text_field("generic_name")
        return ProductData.model_validate(drow)
    except Exception as e:
        print(f"Error processing product {row.code}: {e}")
        return ProductData.model_validate(drow, strict=False)


def row_to_breeding_type_and_quantity(row):
    """
    This function uses the PainReportCalculator to compute the breeding type and egg quantity.
    Extracts egg count, caliber, and breeding type from a DataFrame row.

    Args:
        row (pd.Series): Single product row.

    Returns:
        tuple: (egg_count (int), caliber (str), breeding_type (str)) for the given product.
    """
    try:
        product_data = row_to_product_data(row)
        report = pain_report_calculator.PainReportCalculator(product_data)
        quantities = report._get_quantities()
        breeding_types = report._get_breeding_types()
    except ResourceNotFoundException:
        return -2, "not managed", "not managed"

    quantity = quantities.get("laying_hen")
    if not quantity:
        egg_count = -1
        caliber = "no caliber"
    else:
        egg_count = quantity.count
        caliber = quantity.caliber if quantity.caliber else "no caliber"

    breeding_type = breeding_types.get("laying_hen")
    if not breeding_type:
        breeding = "no breeding"
    elif isinstance(breeding_type, str):
        breeding = breeding_type
    else:
        breeding = breeding_type.breeding_type.value

    return egg_count, caliber, breeding


def prepare_egg_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds display-friendly columns for further plotting.

    Args:
        df (pd.DataFrame): Input DataFrame with product and computed data.

    Returns:
        pd.DataFrame: DataFrame with additional columns for display purposes.
    """
    df = df.copy()
    df["egg_count_string"] = df["egg_count"].apply(
        lambda egg_count: "no count" if egg_count == -1 else "not managed" if egg_count == -2 else "count found"
    )
    df["french_string"] = df["french"].apply(lambda x: "french" if x else "not french")
    return df


def plot_egg_sunburst(dataset: str, include_caliber: bool, eggs_df: pd.DataFrame) -> None:
    """
    Plots a sunburst chart to visualize the part of eggs for which breeding type and quantity are known.

    Args:
        dataset (str): Either "world" for all eggs or "france" for French eggs only.
        include_caliber (bool): Whether to include egg calibers in addition to the egg count.
        eggs_df (pd.DataFrame): Full eggs DataFrame.
    """
    if dataset == "world":
        df = eggs_df
        title_prefix = "All eggs (World)"
        base_path = [px.Constant("all"), "french_string", "breeding", "egg_count_string"]
    elif dataset == "france":
        df = eggs_df[eggs_df["french"]].copy()
        title_prefix = "French eggs"
        base_path = [px.Constant("all"), "breeding", "egg_count_string"]
    else:
        raise ValueError("dataset must be one of ['world', 'france']")

    path = base_path.copy()
    if include_caliber:
        path.append("caliber")

    trace_kwargs = dict(
        texttemplate="%{label}<br>%{percentRoot:.1%}<br>%{value}",
        textfont=dict(size=12),
        insidetextorientation="horizontal",
    )
    layout_kwargs = dict(width=500, height=500, margin=dict(t=40, l=10, r=10, b=10))

    fig = px.sunburst(df, path=path)
    fig.update_traces(**trace_kwargs)
    fig.update_layout(title=f"{title_prefix} : {'with' if include_caliber else 'without'} caliber", **layout_kwargs)
    fig.show()


def parse_arguments():
    """
    Parse command line arguments for the script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process egg product data with OCR predictions and calculate breeding types"
    )

    parser.add_argument(
        "--dataset",
        choices=["world", "france"],
        default="france",
        help="Dataset to visualize: 'world' for all eggs or 'france' for French eggs only (default: france)",
    )

    parser.add_argument("--include-caliber", action="store_true", help="Include egg calibers in the sunburst chart")

    parser.add_argument("--no-plot", action="store_true", help="Disable sunburst chart display")

    parser.add_argument(
        "--no-process", action="store_true", help="Skip data processing and load already processed file"
    )

    return parser.parse_args()


def main():
    """
    Main execution function: loads data, processes it, saves results, and plots.
    """
    args = parse_arguments()

    if args.no_process:
        # Load already processed data
        processed_file = DATA_PATH / "processed_products.csv"
        if not processed_file.exists():
            print(f"Error: Processed file {processed_file} not found. Run without --no-process first.")
            return

        print(f"Loading already processed data from {processed_file}")
        eggs_df = pd.read_csv(processed_file)

        # Load JSON columns if needed
        with open(COLS_TO_JSON_PATH, "r") as f:
            cols_to_json = json.load(f)
        for col in cols_to_json:
            if col in eggs_df.columns:
                eggs_df[col] = eggs_df[col].apply(safe_json_loads)

        print(f"Loaded processed data with {len(eggs_df)} rows")
    else:
        # Full processing pipeline
        eggs_df = load_eggs_df()
        print(f"Loaded eggs_df with {len(eggs_df)} rows")

        code_ocr = create_dataframe_from_jsonl(JSONL_FILE_PATH)
        print(f"Loaded OCR data with {len(code_ocr)} rows")

        eggs_df = enrich_eggs_with_ocr(eggs_df, code_ocr)

        eggs_df[["egg_count", "caliber", "breeding"]] = eggs_df.apply(
            lambda row: pd.Series(row_to_breeding_type_and_quantity(row)), axis=1
        )

        eggs_df.to_csv(DATA_PATH / "processed_products.csv", index=False)
        print(f"Saved processed data to {DATA_PATH / 'processed_products.csv'}")

    # Add french column if not present
    if "french" not in eggs_df.columns:
        eggs_df["french"] = (
            eggs_df["countries_tags"].fillna("").apply(lambda x: "en:france" in x if len(x) > 0 else False)
        )

    # Save French subset if processing was done
    if not args.no_process:
        eggs_df[eggs_df["french"]].to_csv(DATA_PATH / "processed_products_fr.csv", index=False)
        print(f"Saved French subset to {DATA_PATH / 'processed_products_fr.csv'}")

    eggs_df = prepare_egg_display_columns(eggs_df)

    # Plot according to command line arguments
    if not args.no_plot:
        plot_egg_sunburst(args.dataset, args.include_caliber, eggs_df)
        print(
            f"Sunburst chart displayed for {args.dataset} dataset, caliber\
                  {'included' if args.include_caliber else 'excluded'}"
        )
    else:
        print("Chart display disabled")


if __name__ == "__main__":
    main()
