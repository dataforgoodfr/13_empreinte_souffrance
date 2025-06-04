#import tensorflow as tf
#from non_used_models.xgfood.xgfood import XGFood
#from models_categorie.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer import data, encoders, trainer, cleaner, predictor
from models.lewagon_ocr.OpenFoodFactsCategorizer.predictor import Predictor
from models.lewagon_ocr.OpenFoodFactsCategorizer.cleaner import Cleaner
import requests
from models.lewagon_ocr.OpenFoodFactsCategorizer.data import get_data_from_ocr
import csv
import pandas as pd
from tqdm import tqdm
import json
import time
import os


class CategoryPredictor:
    def __init__(self, barcode=None):
        self.barcode = barcode
        self.lewagon_off_categorizer = Predictor(barcode if barcode else "placeholder")
        self.lewagon_ocr_cleaner = Cleaner()
        self.predictions = {}
        self._load_lewagon_model()
        self.df = None

        if barcode:
            self.update_barcode(barcode)
            self.load_robotoff_predictions()

    def update_barcode(self, barcode):
        """Updates barcode and refreshes related data"""
        self.barcode = barcode
        self.lewagon_off_categorizer.barcode = barcode
        self.lewagon_off_categorizer.text = self.lewagon_off_categorizer._get_text_for_barcode()
        self.load_robotoff_predictions()
        time.sleep(1)  # Sleep after barcode update to respect API limits

    def _load_csv(self, path="data/dfoeufs.csv"):
        try:
            self.df = pd.read_csv(path)
            print("[DEBUG] CSV loaded successfully with shape:", self.df.shape)
            return self.df
        except FileNotFoundError:
            print("[ERROR] CSV file not found at:", path)
        except Exception as e:
            print(f"[ERROR] Failed to load CSV: {e}")
        return None

    def _load_lewagon_model(self):
        self.lewagon_off_categorizer.load_model()
        print("[DEBUG] LeWagon model loaded successfully!")

    def load_robotoff_predictions(self):
        url = f"https://robotoff.openfoodfacts.org/api/v1/predictions?barcode={self.barcode}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[ERROR] Robotoff API returned status code {response.status_code}")
            self.predictions = {}
        else:
            self.predictions = response.json()
        time.sleep(1)  # Sleep after Robotoff API call

    def keras_category_classifier_v3_extract_breeding_type(self):
        """Extracts breeding type from Robotoff predictions"""
        for pred in self.predictions.get("predictions", []):
            if pred.get("type") != "category":
                continue
            if pred.get("value_tag") == "en:chicken-eggs":
                neighbors = pred.get("data", {}).get("neighbor_predictions", {})
                children = neighbors.get("children", {})
                sorted_children = sorted(
                    [(k, v) for k, v in children.items() if v is not None],
                    key=lambda x: x[1],
                    reverse=True,
                )
                if sorted_children:
                    return sorted_children[:3]  # Return top 3 (tag, confidence)
        return None

    def lewagon_off_prediction(self):
        """Predict category using LeWagon model"""
        prediction = self.lewagon_off_categorizer.predict(threshold=0.012)
        time.sleep(0.5)  # Sleep after LeWagon prediction call
        return prediction

    def lewagon_off_ocr_text(self, n_images=3):
        """Returns OCR text from the first n images of the product"""
        text = []
        for i in range(1, n_images + 1):
            try:
                url = self.lewagon_off_categorizer._get_image_folder_url()
                if url:
                    url = url + f'/{i}.json'
                    ocr_text_per_page = get_data_from_ocr(url)
                    text.append(ocr_text_per_page)
                time.sleep(0.5)
            except Exception as e:
                print(f"[ERROR] Unable to get OCR text from page number {i}: {e}")
                continue
        if text:
            return ' '.join(text)
        else:
            print(f"[ERROR] No OCR text found for {self.barcode}")
            return None

    def make_single_prediction(self):
        return {
            "predictions": {
                "lewagon_prediction": self.lewagon_off_prediction(),
                "keras_category_classifier_v3_prediction": self.keras_category_classifier_v3_extract_breeding_type(),
            },
            "ocr_text": {
                "off": self.lewagon_off_ocr_text()
            }
        }

    def make_batch_prediction(self, csv_path="data/dfoeufs.csv", output_path="data/dfoeufs_with_predictions_with_ground_truth.csv"):
        self._load_csv(csv_path)
        if self.df is None:
            print("[ERROR] No data to process.")
            return

        jsonl_output_path = output_path.replace(".csv", ".jsonl")
        processed_barcodes = set()

        # Build lookup dict for ground truth breeding from self.df
        code_to_breeding = dict(zip(self.df['code'].astype(str), self.df['breeding']))

        # Load already processed barcodes from JSONL if exists
        if os.path.exists(jsonl_output_path):
            with open(jsonl_output_path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        processed_barcodes.add(entry.get("code"))
                    except json.JSONDecodeError:
                        print("[WARN] Skipping corrupt line in JSONL")

        with open(jsonl_output_path, "a", encoding="utf-8") as jsonl_file:
            for _, row in tqdm(self.df.iterrows(), total=len(self.df)):
                barcode = str(row["code"])

                if barcode in processed_barcodes:
                    continue  # Skip already processed barcode

                result = {
                    "code": barcode,
                    "lewagon_prediction": None,
                    "keras_category_classifier_v3_prediction": None,
                    "ocr_text": None,
                    "ground_truth": code_to_breeding.get(barcode, None),  # Add ground truth here
                }

                try:
                    self.update_barcode(barcode)
                except Exception as e:
                    print(f"[WARN] Failed to update barcode {barcode}: {e}")
                    jsonl_file.write(json.dumps(result, ensure_ascii=False) + "\n")
                    continue

                try:
                    result["lewagon_prediction"] = self.lewagon_off_prediction()
                except Exception as e:
                    print(f"[WARN] LeWagon prediction failed for {barcode}: {e}")

                try:
                    result["keras_category_classifier_v3_prediction"] = self.keras_category_classifier_v3_extract_breeding_type()
                except Exception as e:
                    print(f"[WARN] Robotoff prediction failed for {barcode}: {e}")

                try:
                    result["ocr_text"] = self.lewagon_off_ocr_text()
                except Exception as e:
                    print(f"[WARN] OCR text extraction failed for {barcode}: {e}")

                jsonl_file.write(json.dumps(result, ensure_ascii=False) + "\n")

        print(f"[INFO] Batch prediction complete. JSONL saved to {jsonl_output_path}")



predictor = CategoryPredictor()
print(predictor.make_batch_prediction())
