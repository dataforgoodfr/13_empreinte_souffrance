FROM python:3.8-slim

WORKDIR /app

# Copy specific files and folders (only those allowed by .dockerignore)
COPY testing_cat_models.py requirements.txt ./ 
COPY models_categorie/lewagon_ocr_OpenFoodFactsCategorizer models_categorie/lewagon_ocr_OpenFoodFactsCategorizer
COPY data/ ./data/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y bash

CMD ["python"]
