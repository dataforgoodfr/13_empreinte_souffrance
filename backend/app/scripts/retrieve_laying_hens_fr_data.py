"""
Fetches poultry farming data from georisques.gouv.fr API, processes it,
and exports to JSON/CSV with caching.
"""

import csv
import json
import os
from typing import Dict, List

import requests

# Config
API_URL = "https://georisques.gouv.fr/api/v1/installations_classees"
RAW_JSON_FILE = "raw_data.json"
POULTRY_JSON_FILE = "volailles_sorted.json"
POULTRY_CSV_FILE = "volailles_details.csv"
POULTRY_SUMMARY_CSV = "volailles_synthese.csv"

# API parameters
params = {
    "page": 1,
    "page_size": 1000,
    "activite": "01",  # NAF v2 code - "Culture et production animale, chasse et services annexes"
}
headers = {"accept": "application/json"}


def fetch_all_pages() -> List[Dict]:
    """Fetches all paginated data from API"""
    data = []
    current_page = 1

    print("Fetching API data...")
    while True:
        print(f"  Processing page {current_page}...")
        response = requests.get(API_URL, params=params, headers=headers)

        if response.status_code != 200:
            print(f"Error: API request failed with status {response.status_code}")
            break

        page_data = response.json()
        data.extend(page_data.get("data", []))

        if not page_data.get("next"):
            break

        params["page"] += 1
        current_page += 1

    print(f"\nTotal records fetched: {len(data)}")
    return data


def save_json(data: List[Dict], filename: str) -> None:
    """Saves data to JSON file"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")


def load_json(filename: str) -> List[Dict]:
    """Loads data from JSON file"""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def get_poultry_count(entry: Dict) -> float:
    """Extracts poultry count from rubrique 2111"""
    for rubric in entry.get("rubriques", []):
        # 2111 is an ICPE code - "Volailles, gibiers à plumes"
        if rubric.get("numeroRubrique") == "2111":
            try:
                return float(rubric.get("quantiteTotale", 0))
            except ValueError:
                return 0
    return 0


def process_data(data: List[Dict]) -> List[Dict]:
    """Processes data and filters poultry farms"""
    processed = []

    print("\nProcessing data...")
    for idx, entry in enumerate(data, 1):
        if entry.get("volailles"):
            entry["volailles_count"] = get_poultry_count(entry)
            processed.append(entry)

        if idx % 1000 == 0:
            print(f"  Processed {idx} records...")

    # Sort by descending poultry count
    processed.sort(key=lambda x: x["volailles_count"], reverse=True)
    return processed


def export_summary_csv(data: List[Dict]) -> None:
    """Exports synthetic data to CSV"""
    if not data:
        print("No data to export!")
        return

    # Define field names
    fieldnames = [
        "Nombre d'animaux",
        "raison sociale",
        "adresse 1",
        "code postal",
        "code insee",
        "commune",
        "longitude",
        "latitude",
        "siret",
        "Nombre total d'inspections",
        "Nombre de document d'inspection",
        "Nombre de document hors inspection",
        "date_maj",
    ]

    print("\nExport synthetic CSV...")
    with open(POULTRY_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for idx, entry in enumerate(data, 1):
            inspections = entry.get("inspections", [])
            docs_inspection = sum(1 for i in inspections if i.get("fichierInspection"))

            row = {
                "Nombre d'animaux": entry.get("volailles_count", 0),
                "raison sociale": entry.get("raisonSociale", ""),
                "adresse 1": entry.get("adresse1", ""),
                "code postal": entry.get("codePostal", ""),
                "code insee": entry.get("codeInsee", ""),
                "commune": entry.get("commune", ""),
                "longitude": entry.get("longitude", 0),
                "latitude": entry.get("latitude", 0),
                "siret": entry.get("siret", ""),
                "Nombre total d'inspections": len(inspections),
                "Nombre de document d'inspection": docs_inspection,
                "Nombre de document hors inspection": len(entry.get("documentsHorsInspection", [])),
                "date_maj": entry.get("date_maj", ""),
            }

            writer.writerow(row)

            if idx % 1000 == 0:
                print(f"  Exported {idx} records...")

    print(f"CSV export completed: {POULTRY_SUMMARY_CSV}")


def export_to_csv(data: List[Dict]) -> None:
    """Exports data to CSV"""
    if not data:
        print("No data to export!")
        return

    # Collect all field names from the data
    fieldnames = set()
    for entry in data:
        fieldnames.update(entry.keys())
    fieldnames = list(fieldnames) + ["volailles_count"]

    # Special handling for nested fields
    nested_fields = ["rubriques", "inspections", "documentsHorsInspection"]

    print("\nExporting to CSV...")
    with open(POULTRY_CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for idx, entry in enumerate(data, 1):
            # Flatten nested fields
            row = entry.copy()
            for field in nested_fields:
                if field in row:
                    row[field] = json.dumps(row[field], ensure_ascii=False)

            writer.writerow(row)

            if idx % 1000 == 0:
                print(f"  Exported {idx} records...")

    print(f"CSV export completed: {POULTRY_CSV_FILE}")


def main():
    # Try to load cached data
    if os.path.exists(RAW_JSON_FILE):
        print("Loading cached data...")
        all_data = load_json(RAW_JSON_FILE)
    else:
        all_data = fetch_all_pages()
        save_json(all_data, RAW_JSON_FILE)

    # Process and filter data
    poultry_data = process_data(all_data)
    save_json(poultry_data, POULTRY_JSON_FILE)

    # Export to CSV
    export_to_csv(poultry_data)
    export_summary_csv(poultry_data)


if __name__ == "__main__":
    main()
