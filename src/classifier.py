import json
import os
from os.path import join as opj
from typing import Any, Sequence, Union

from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from src.settings.classifier import ClassifierSettings, PredictOutput


class Classifier:
    def __init__(self, model_settings: ClassifierSettings, vectorizer=None, model=None):
        self.vectorizer = vectorizer if vectorizer else TfidfVectorizer()
        self.model = (
            model
            if model
            else RandomForestClassifier(
                n_estimators=model_settings.n_estimators,
                max_depth=model_settings.max_depth,
            )
        )
        self.id2label = model_settings.id2label

    def fit(self, X: Sequence[str], y: Sequence[Any]):
        X_transformed = self.vectorizer.fit_transform(X)
        self.model.fit(X_transformed, y)

    def predict(self, X: Union[str, Sequence[str]]) -> PredictOutput:
        if isinstance(X, str):
            X = [X]
        X_transformed = self.vectorizer.transform(X)
        numeric_predictions = self.model.predict(X_transformed)

        text_predictions = [self.id2label[id] for id in numeric_predictions]
        if len(text_predictions) == 1:
            return PredictOutput(sentiment=text_predictions[0])
        return PredictOutput(sentiment=text_predictions)

    def save(self, save_path: str):
        os.makedirs(save_path, exist_ok=True)
        model_path = opj(save_path, "model.joblib")
        vectorizer_path = opj(save_path, "vectorizer.joblib")
        settings_path = opj(save_path, "settings.json")

        dump(self.model, model_path)
        dump(self.vectorizer, vectorizer_path)
        with open(settings_path, 'w') as f:
            json.dump({
                "n_estimators": self.model.get_params()["n_estimators"],
                "max_depth": self.model.get_params()["max_depth"],
                "id2label": self.id2label
            }, f)

    @classmethod
    def load(cls, load_path: str):
        model_path = opj(load_path, "model.joblib")
        vectorizer_path = opj(load_path, "vectorizer.joblib")
        settings_path = opj(load_path, "settings.json")  # Путь к файлу настроек
        
        model = load(model_path)
        vectorizer = load(vectorizer_path)
        
        # Загрузка настроек модели из JSON
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        model_settings = ClassifierSettings(
            n_estimators=settings["n_estimators"],
            max_depth=settings["max_depth"],
            id2label=settings["id2label"]
        )
        
        return cls(model_settings=model_settings, vectorizer=vectorizer, model=model)
