import os
import pandas as pd
import requests

from sklearn.model_selection import train_test_split


# Get data to use our ridge model

def get_data_from_ocr(url):
    """Expects url to a json ocr -from image- """
    result = requests.get(url)
    json = result.json()
    text = json['responses'][0]['fullTextAnnotation']['text']
    return text


### Get data to train a new model

def get_data(path='.'):
    # set the path in parameters
    df = pd.read_csv(path)

    return df

def get_data_from_text(path='.', holdout=0.3):
    # set the path in parameters
    """To train a new model.
    Expects a path to a csv with ocr text and labels; Returns splitted train-test data"""
    df = pd.read_csv(path)
    #X = #???
    #y = #???
    X= df['clean_text']
    y = df['pnns_groups_2']
    train_test_split(X, y, test_size=holdout)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 1)
    return X_train, X_test, y_train, y_test



#if __name__ == '__main__':
#print(get_data_from_ocr('https://static.openfoodfacts.org/images/products/00390804/1.json'))
