from src.settings.base import ExtraFieldsNotAllowedBaseModel


class PreprocessorSettings(ExtraFieldsNotAllowedBaseModel):
    use_normalization: bool = True
    use_lemmatization: bool = True
