import pytest

from src.preprocessor import Preprocessor
from src.settings.preprocessor import PreprocessorSettings


@pytest.fixture
def sample_text():
    return "This is    a sample text! Áccented characters?"

@pytest.fixture
def preprocessor():
    settings = PreprocessorSettings(use_normalization=True, use_lemmatization=False)
    return Preprocessor(settings)

def test_normalize_text(preprocessor, sample_text):
    normalized_text = preprocessor.normalize_text(sample_text)
    assert " " in normalized_text
    assert "Á" not in normalized_text
    assert normalized_text == "This is a sample text! Accented characters?"

def test_lemmatize_text(preprocessor, sample_text):
    preprocessor.settings.use_lemmatization = True
    lemmatized_text = preprocessor.lemmatize_text("corpora")
    assert lemmatized_text == "corpus"

def test_full_preprocess(preprocessor, sample_text):
    preprocessed_text = preprocessor(sample_text)
    assert " " in preprocessed_text
