from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import cross_val_score
import joblib
from models_categorie.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.helpers import list_categories
from models_categorie.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.encoders import CustomPreprocessor
from models_categorie.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.data import get_data
from models_categorie.lewagon_ocr_OpenFoodFactsCategorizer.OpenFoodFactsCategorizer.data import get_data_from_text


class Trainer():

    def __init__(self, X, y):
        self.pipeline = None
        self.X = X
        self.y = y
        self.list_cat = list_categories


    def create_pipeline(self):
        """Returns a full pipeline with preprocessing and model"""
        nltk.download('stopwords')
        stop_words = set(stopwords.words('french'))
        self.pipeline = Pipeline([
            ("custom_preprocessor", CustomPreprocessor()),
            ("tfidf", TfidfVectorizer(ngram_range=(2, 2), stop_words=stop_words)),
            ("ridge", RidgeClassifier())
        ])

    def train_model(self):
        """Requires a created pipeline; Returns a trained pipeline"""
        self.create_pipeline()

        return self.pipeline.fit(self.X, self.y)


    def evaluate_model(self, X_test, y_test):
        """Expects a trained pipeline; Returns a cross-validated score for the trained pipeline"""
        return cross_val_score(self.pipeline,
                        X_test, y_test,
                        scoring="accuracy",
                        n_jobs=-1) \
                    .mean()

    def save_model(self, filename="model2.joblib"):
        """Saves the current pipeline if needed"""
        joblib.dump(self.pipeline, filename)

        return None

if __name__ == '__main__':
    # choose which steps are needed
    X_train, X_test, y_train, y_test = get_data_from_text()
    trainer = Trainer(X=X_train, y=y_train)
    trainer.train_model()
    trainer.evaluate_model(X_test, y_test)
    trainer.save_model()




