import re
import unicodedata

from textblob import TextBlob

from src.settings.preprocessor import PreprocessorSettings


class Preprocessor:
    def __init__(self, settings: PreprocessorSettings):
        self.settings = settings

    def normalize_text(self, text: str) -> str:
        text = re.sub(r"[ \t]+", " ", text)
        text = "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )
        return text

    def lemmatize_text(self, text: str) -> str:
        blob = TextBlob(text)
        return " ".join([word.lemmatize() for word in blob.words])

    def preprocess(self, text: str) -> str:
        if self.settings.use_normalization:
            text = self.normalize_text(text)
        if self.settings.use_lemmatization:
            text = self.lemmatize_text(text)
        return text

    def __call__(self, text: str) -> str:
        return self.preprocess(text)
