import pytest
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split

from src.classifier import Classifier
from src.settings.classifier import ClassifierSettings


@pytest.fixture(scope="module")
def data():
    X_train = ["This is about atheism", "This is about religion"]
    y_train = [0, 1]
    X_test = ["Religion topic", "Atheism topic"]
    y_test = [1, 0]
    return X_train, X_test, y_train, y_test

@pytest.fixture(scope="module")
def classifier_settings():
    return ClassifierSettings(n_estimators=2, max_depth=1, id2label={0: 'alt.atheism', 1: 'soc.religion.christian'})

@pytest.fixture(scope="module")
def trained_classifier(data, classifier_settings):
    X_train, _, y_train, _ = data
    classifier = Classifier(model_settings=classifier_settings)
    classifier.fit(X_train, y_train)
    return classifier

def test_classifier_save_load(tmp_path, trained_classifier, data):
    save_path = tmp_path / "classifier"
    trained_classifier.save(str(save_path))
    loaded_classifier = Classifier.load(str(save_path))

    assert loaded_classifier is not None
    assert hasattr(loaded_classifier, 'model')
    assert hasattr(loaded_classifier, 'vectorizer')

    
    _, X_test, _, y_test = data
    predictions = loaded_classifier.predict(X_test)
    
    assert len(predictions.sentiment) == len(y_test)
    assert all(pred in loaded_classifier.id2label.values() for pred in predictions.sentiment), "Все предсказания должны быть текстовыми метками."
