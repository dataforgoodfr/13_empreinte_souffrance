# Neural Category Predictions

This repository contains models for OCR and machine learning-based category prediction, along with scripts to run them and associated data (recognized texts and classification outputs).

## Scripts

- **`generate_predictions.py`**
  Generates a JSONL file containing predictions from two models:
  - `lewagon_ocr` (runs locally)
  - `keras-category-classifier-image-embeddings-3.0` (runs via API)

  It also performs OCR on up to the first three images associated with a product via its barcode.
  Each line in the output file follows this format:

  ```json
  {
    "code": "12345678",
    "lewagon_prediction": {
      "proba_1": "eggs",
      "confidence_1": 0.0984,
      ...
    },
    "keras_category_classifier_v3_prediction": [
      ["en:free-range-chicken-eggs", 0.3200766444206238],
      ["en:barn-chicken-eggs", 0.014705373905599117],
      ["en:cage-chicken-eggs", 0.0]
    ],
    "ocr_text": "10 CADROJAC\nFR\n(31.091.010)\nCE\npc10\nSovivo\nCovivo 31....",
    "ground_truth": "free_range"
  }

The approximate time to go through the whole database is around 10 hours due to API use constraints.

### Running `lewagon_ocr` (Legacy Model)

Because `lewagon_ocr` is a legacy model, it must be run inside a Docker container.

At the root of the repository, use the following commands:

- **To build the Docker image:**
  ```bash
  docker build -t cat-predictor .
- **To run:**
    ```bash
    docker run -it --rm cat-predictor bash

- **To compose with shell**
    ```bash
    docker-compose run app /bin/bash

With the latter you'll be able to run python commands just like you would do without Docker.

IMPORTANT: `requirements_legacy.txt` are for the legacy lewagon model! These are not the actual dependencies.

To run the two other scripts, use `poetry install` !

- **prediction_statistics.py** -> prints statistics about `data/dfoeufs_with_predictions_with_ground_truth.jsonl` and `data/dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl`

- **groq_extract_spans.py** -> generates a new file `data/dfoeufs_with_predictions_with_ground_truth_with_groq.jsonl` where each line has a new key:

```json
{"groq_spans":
{"breeding_type_related": "Poules élevées Liberté...",
"weight_related": "100g, énergie 584kJ/140kcal, matières grasses 9,8g, glucides 0, protéines 12,7g, sel0,3g"}
}

This script extracts relevant fragments from the OCR-generated texts on the packaging with the help of an LLM.
To run it you need to have your own Groq API key.

Once you obtained it, at the root of this folder create .env
and put

    ```bash
    GROQ_API_KEY=YOUR_API_KEY
    GROQ_API_BASE=https://api.groq.com/openai/v1

Beware of the token limits if you use a free plan!
