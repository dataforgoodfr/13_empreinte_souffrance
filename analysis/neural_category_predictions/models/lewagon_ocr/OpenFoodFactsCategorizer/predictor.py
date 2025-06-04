import joblib
import numpy as np
from models.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.helpers import list_categories
from models.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.cleaner import Cleaner
from models.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.data import get_data_from_ocr
import os
import requests
from urllib.parse import urlparse

# Assumes you already have Cleaner and get_data_from_ocr, list_categories defined somewhere
# from your_module import Cleaner, get_data_from_ocr, list_categories

class Predictor:
    model = None
    _cached_barcode = None
    _cached_ocr_text = None
    _cached_text = None

    def __init__(self, barcode):
        self.cleaner = Cleaner()
        self.barcode = barcode
        self.load_model()
        self.text = self._get_text_for_barcode()

    def load_model(self):
        if Predictor.model is None:
            model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'bestridge_compressed.joblib'))
            Predictor.model = joblib.load(model_path)
            print("[INFO] Model loaded from:", model_path)
        self.model = Predictor.model

    def _get_text_for_barcode(self):
        if Predictor._cached_barcode == self.barcode:
            print("[INFO] Using cached OCR text for barcode:", self.barcode)
            return Predictor._cached_text

        print("[INFO] Fetching OCR text for barcode:", self.barcode)
        image_url = self._get_image_folder_url()
        if not image_url:
            print("[WARNING] Could not retrieve image folder for barcode:", self.barcode)
            return ""

        ocr_data = get_data_from_ocr(image_url + '/1.json')
        cleaned_text = self.cleaner.clean_ocr_text(text=ocr_data, spellcheck=None)

        # Cache results
        Predictor._cached_barcode = self.barcode
        Predictor._cached_ocr_text = ocr_data
        Predictor._cached_text = cleaned_text

        return cleaned_text

    def _get_image_folder_url(self):
        product_url = f"https://world.openfoodfacts.org/api/v0/product/{self.barcode}.json"
        response = requests.get(product_url)
        if response.status_code != 200:
            print(f"[ERROR] Product API returned {response.status_code} for barcode {self.barcode}")
            return None

        data = response.json()
        if data.get("status") != 1:
            print(f"[ERROR] Product not found for barcode {self.barcode}")
            return None

        front_img_url = data.get("product", {}).get("image_front_url")
        if not front_img_url:
            print(f"[ERROR] No front image found for product {self.barcode}")
            return None

        parsed = urlparse(front_img_url)
        folder_path = os.path.dirname(parsed.path)
        folder_url = f"{parsed.scheme}://{parsed.netloc}{folder_path}"
        return folder_url

    def predict(self, threshold=0.012, top_n=3):
        if not self.text:
            print("[ERROR] No OCR text available to make prediction.")
            return None

        d = self.model.decision_function([self.text])
        probs = np.exp(d) / np.sum(np.exp(d), axis=1, keepdims=True)
        proba = list(probs[0])
        sorted_indices = np.argsort(proba)[::-1]

        list_cat = list_categories
        result = {}
        for i in range(min(top_n, len(proba))):
            result[f"proba_{i+1}"] = list_cat[sorted_indices[i]]
            result[f"confidence_{i+1}"] = round(proba[sorted_indices[i]], 4)

        return result





#if __name__ == '__main__':

    #predictor = Predictor(text=Predictor.text)
    #predictor.load_model()
    #print(predictor.predict(threshold=0.012))
