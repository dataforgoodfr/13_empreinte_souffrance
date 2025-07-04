from model2vec.train import StaticModelForClassification
from utils.load_dataset import train_test_dataset, load_dataset
import yaml
from pathlib import Path
from sklearn.model_selection import KFold
import pandas as pd
import os
import numpy as np

class Evaluator:
    def __init__(self, dataset_name):
        self._load_config()
        self.model_name = self.config["model"]["name"]
        self.model = self._load_model()
        self.dataset_name = dataset_name
        self.data_path = Path(__file__).resolve().parent.parent / self.config["dataset"][self.dataset_name]["path"]
        self.evaluation_results_path = f"evaluation_results/{self.dataset_name}_fold_class_accuracies.csv"

    def _load_config(self, path="config.yaml"):
        with open(path, "r") as f:
            self.config = yaml.safe_load(f)

    def _load_model(self):
        print(f"Loading model: {self.model_name}")
        return StaticModelForClassification.from_pretrained(model_name=self.model_name)

    def evaluate(self):
        print("Loading dataset...")
        X_train, X_test, y_train, y_test = train_test_dataset(
            input_file=self.data_path,
            Xcol=self.config["dataset"][self.dataset_name]["X_col"],
            ycol=self.config["dataset"]["y_col"],
            test_size=self.config["dataset"].get("train_test_split", 0.15)
        )

        print("Training model...")
        self.model.fit(X_train, y_train)

        print("Evaluating model...")
        results = self.model.evaluate(X_test, y_test)
        return results

    def evaluate_k_fold(self):
        self.k_fold = self.config["evaluation"]["k_fold"]
        X, y = load_dataset(
            input_file=self.data_path,
            Xcol=self.config["dataset"][self.dataset_name]["X_col"],
            ycol=self.config["dataset"]["y_col"],
            supervised=True
        )

        kf = KFold(n_splits=self.k_fold, shuffle=True, random_state=42)
        fold = 1
        all_accuracies = {}
        for train_index, test_index in kf.split(X):
            print(f"Fold {fold}:")

            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            self.model = self._load_model()

            print("Training model...")
            self.model.fit(X_train, y_train)

            print("Evaluating model...")
            y_hat = self.model.predict(X_test)

            classes = np.unique(y_test)
            class_accuracies = {}
            for cls in classes:
                idx = (y_test == cls)
                class_acc = np.mean(y_hat[idx] == y_test[idx]) * 100
                class_accuracies[cls] = class_acc
            all_accuracies[fold] = class_accuracies
            fold += 1

        os.makedirs("evaluation_results", exist_ok=True)
        df_results = pd.DataFrame.from_dict(all_accuracies, orient='index')
        df_results.index.name = 'fold'
        df_results.reset_index(inplace=True)
        df_results.to_csv(self.evaluation_results_path, index=False)

        print("Saved evaluation results to evaluation_results/fold_class_accuracies.csv")

        return all_accuracies

    def evaluation_stats(self):
        try:
            dataframe = pd.read_csv(self.evaluation_results_path)
            mean_accuracies = dataframe.drop(columns=['fold']).mean().to_dict()
            return mean_accuracies
        except FileNotFoundError:
            print("Evaluation file does not exist")
            return {}

if __name__ == "__main__":
    dataset_name = input("Which dataset do you want to evaluate? (full_ocr / span_ocr): ").strip()
    if dataset_name not in {"full_ocr", "span_ocr"}:
        raise ValueError("Invalid dataset name. Please choose 'full_ocr' or 'span_ocr'.")

    evaluator = Evaluator(dataset_name=dataset_name)
    print(evaluator.evaluation_stats())
