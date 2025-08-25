# Classification model
This project implements a classification model pipeline for predicting labels such as "barn," "free_range," and "furnished_cage" from text data. It includes:

- **Data loading and preprocessing**: Clean and prepare datasets from CSV/JSONL files.

- **Model training and evaluation**: Train a StaticModelForClassification model using configurable parameters.

- **K-fold cross-validation**: Perform robust evaluation with detailed per-class accuracy metrics saved as CSV.

- **Evaluation stats**: Summarize results across folds, computing mean accuracy per class.

- ***Pushing the model directly to HuggingFace***: The fine-tuned StaticModelForClassification will be saved to HF-hub.



## Installation
The project uses ```uv``` for dependency management and is designed to separate research experiments from backend and frontend code.
1. Install uv (if not installed)
```
pip install uv
```

2. Navigate to the project folder
```
cd path/to/project/
```

3. Install dependencies from the uv lock file
```
uv sync
```
- This reads the uv.lock file and installs all the pinned packages into a virtual environment.
- It will create a .venv folder inside the project directory by default.

4. Activate the virtual environment
```
uv shell
```
- This drops you into the project’s virtual environment.
- From here, you can run scripts like python model_manager.py.

## Model Manager Use
Run the model manager interactively:
```
poetry run python model_manager.py
```

### Step 1: Choose Dataset
You can choose between ```full_ocr``` and ```span_ocr```: the former uses full OCR-deciphered texts from packaging and the latter uses only breeding-related textual spans.

### Step 2: Training and Evaluation
- Loads the specified dataset.
- Detects the classes automatically.
- Fits the model using StaticModelForClassification.
- Optionally saves the trained model in saved_model/.

### Step 3: Save Class Mapping

The class names are stored in saved_model/classes.json to ensure correct label mapping. By default, model2vec puts them in an alphabetic order and assigns numbers from 0 to the length of the class list minus 1.

### Step 4: Push to Hugging Face
After training, the model can be pushed to HF:
```
evaluator.push_to_hf()
```
Creates the repo if it doesn’t exist.

### Optional: K-Fold Cross-Validation
```
evaluator.evaluate_k_fold()
```
- Returns per-fold, per-class accuracy.
- Saves results to evaluation_results/<dataset_name>_fold_class_accuracies.csv.

### Optional: Evaluation with Synthetic Data
```
evaluator.evaluate_with_synth_data()
```
- Combines real and synthetic data at fractions [0.1, 0.25, 0.5, 1.0].
- Evaluates model performance on the test set.

### Optional: Compute Statistics
```
evaluator.evaluation_stats()
```
Returns the mean accuracy per class across folds.

## Hugging Face Model Use
An example of the saved HF model is in ```model_test.py```.
This example shows how to load a pretrained StaticModelForClassification from Hugging Face and run predictions on new text data.

```
from model2vec.train import StaticModelForClassification
from huggingface_hub import hf_hub_download
import json
```

1. Load the pretrained model
We load the model directly from Hugging Face using ```from_pretrained```. The out_dim=3 tells the model that there are three classes in total.
```
model = StaticModelForClassification.from_pretrained(
    model_name="adeliaKH/breeding_type_classificator",
    out_dim=3
)
```

2. Load the class names
The model internally may only know classes as numbers (0, 1, 2), so we load the original class names from classes.json that was saved with the model.

```
with open("saved_model/classes.json", "r") as f:
    classes = json.load(f)
```

3. Assign the class names to the model
This ensures predictions will return the original, human-readable class labels.
```
model.classes_ = classes
```

4. Run predictions on new text
The predict method takes a list of texts and returns the predicted class for each.
```
texts = ["Example 1"]
preds = model.predict(texts)
print(preds)
```

Output example: ```['barn']```.


## Results
The 5-fold cross-validation showed the following results for the chosen model:
```
{'barn': 90.37315986313361, 'free_range': 97.77584571575056, 'furnished_cage': 93.51558003567848}
```

In another experiment, we made groq extract breeding-related spans from the OCR texts, which led to minimal improvements for two classes and a worse result for the other one:

```
{'barn': 88.63455834721285, 'free_range': 98.8195516330785, 'furnished_cage': 94.1304347826087}
```

When we use synthetic data for minority classes:
```
{0.1: {'barn': 95.34883720930233, 'free_range': 98.9247311827957, 'furnished_cage': 95.55555555555556}, 0.25: {'barn': 93.02325581395348, 'free_range': 99.46236559139786, 'furnished_cage': 91.11111111111111}, 0.5: {'barn': 93.02325581395348, 'free_range': 98.9247311827957, 'furnished_cage': 95.55555555555556}, 1.0: {'barn': 97.67441860465115, 'free_range': 98.38709677419355, 'furnished_cage': 97.77777777777777}}
```


## Resources
- Documentation for model2vec: https://github.com/MinishLab/model2vec/blob/main/docs/usage.md
