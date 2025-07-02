# Classification model
This project implements a classification model pipeline for predicting labels such as "barn," "free_range," and "furnished_cage" from text data. It includes:

**Data loading and preprocessing**: Clean and prepare datasets from CSV/JSONL files.

**Model training and evaluation**: Train a StaticModelForClassification model using configurable parameters.

**K-fold cross-validation**: Perform robust evaluation with detailed per-class accuracy metrics saved as CSV.

**Evaluation stats**: Summarize results across folds, computing mean accuracy per class.

The project uses Poetry for dependency management and is designed to separate research experiments from backend and frontend code.

## Installation

This project requires setting up a separate venv from backend. When installing poetry, it might automatically try to use Python from backend.
- To deactivate it, you can either do ```deactivate``` or, if no such command is found or permission is denied ```unset VIRTUAL_ENV``` and then ```hash -r```. You might want to reload the terminal.
- To make sure that you're out of the backend venv, run ```which python``` and ```python --version```.
- Go to the task folder: ```cd research_development/neural_category_predictions/02_task_classification_model```
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


## Resources
- Documentation for model2vec: https://github.com/MinishLab/model2vec/blob/main/docs/usage.md
