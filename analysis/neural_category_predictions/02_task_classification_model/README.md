# Classification model
This project implements a classification model pipeline for predicting labels such as "barn," "free_range," and "furnished_cage" from text data. It includes:

- **Data loading and preprocessing**: Clean and prepare datasets from CSV/JSONL files.

- **Model training and evaluation**: Train a StaticModelForClassification model using configurable parameters.

- **K-fold cross-validation**: Perform robust evaluation with detailed per-class accuracy metrics saved as CSV.

- **Evaluation stats**: Summarize results across folds, computing mean accuracy per class.

The project uses Poetry for dependency management and is designed to separate research experiments from backend and frontend code.

## Installation

⚠️ Note: This project requires a separate virtual environment from the main backend. The Python version is downgraded to 3.10.12 due to compatibility constraints with torch and numpy.When installing poetry, it might automatically try to use Python from the backend that uses 3.13.

- To deactivate it, you can either do ```deactivate``` or, if no such command is found or permission is denied ```unset VIRTUAL_ENV``` and then ```hash -r```. You might want to reload the terminal.
- To make sure that you're out of the backend venv, run ```which python``` and ```python --version```.
- Go to the task folder: ```cd analysis/neural_category_predictions/02_task_classification_model```
- Set a local python version: ```pyenv local 3.10.12```.
- Make poetry use it too: ```poetry env use /Users/adeliakhasanova/.pyenv/versions/3.10.12/bin/python```
- Now install everything: ```poetry install --no-root```
- NB: sometimes, even though packages are added to poetry, running ```python your_script.py``` doesn't work, in this case, I advise you to do ```poetry run python your_script.py```.

If you want to use any new libraries when working on this project do so through ```poetry add your_library```. It might start a conflict with existing dependencies -- have fun!

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
