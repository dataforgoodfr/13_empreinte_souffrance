import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import yaml


def load_dataset(input_file, Xcol, ycol, supervised=True):
    df = pd.read_csv(input_file).dropna(subset=[Xcol]).set_index("code")
    if supervised:
        df = df[df[ycol] != 'None'].dropna(subset=[ycol])
    return df[Xcol].values, df[ycol].values


def train_test_dataset(input_file, Xcol, ycol, test_size):
    X, y=load_dataset(input_file, Xcol, ycol, supervised=True)
    return train_test_split(X, y, test_size=test_size)
