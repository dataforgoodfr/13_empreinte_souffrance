# Classification model
This project implements a classification model pipeline for predicting labels such as "barn," "free_range," and "furnished_cage" from text data. It includes:

- **Data loading and preprocessing**: Clean and prepare datasets from CSV/JSONL files.

- **Model training and evaluation**: Train a StaticModelForClassification model using configurable parameters.

- **K-fold cross-validation**: Perform robust evaluation with detailed per-class accuracy metrics saved as CSV.

- **Evaluation stats**: Summarize results across folds, computing mean accuracy per class.



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
{0.1: {'barn': 95.34883720930233, 'free_range': 98.9247311827957, 'furnished_cage': 95.55555555555556}, 0.25: {'barn': 93.02325581395348, 'free_range': 99.46236559139786, 'furnished_cage': 91.11111111111111}, 0.5: {'barn': 93.02325581395348, 'free_range': 98.9247311827957, 'furnished_cage': 95.55555555555556}, 1.0: {'barn': 97.67441860465115, 'free_range': 98.38709677419355, 'furnished_cage': 97.77777777777777}}


## Resources
- Documentation for model2vec: https://github.com/MinishLab/model2vec/blob/main/docs/usage.md
