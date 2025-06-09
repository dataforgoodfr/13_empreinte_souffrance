import pandas as pd
from sklearn.model_selection import train_test_split

INPUT_FILE = "data/dfoeufs_with_predictions_with_ground_truth.jsonl"


def load_dataset(input_file=INPUT_FILE, Xcol="ocr_text", ycol="ground_truth", supervised=True):
    df=pd.read_json(input_file, lines=True).dropna(subset=Xcol).set_index("code")
    if supervised:
        df = df[df[ycol] != 'None'].dropna(subset=ycol)
    return df[Xcol].values, df[ycol].values


def train_test_dataset(input_file=INPUT_FILE, Xcol="ocr_text", ycol="ground_truth", test_size=0.15):
    X, y=load_dataset(input_file, Xcol, ycol, supervised=True)
    return train_test_split(X, y, test_size=test_size )
