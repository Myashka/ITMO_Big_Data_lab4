from src.settings.base import ExtraFieldsNotAllowedBaseModel
from src.settings.classifier import ClassifierSettings
from src.settings.preprocessor import PreprocessorSettings


class Config(ExtraFieldsNotAllowedBaseModel):
    preprocessing_config: PreprocessorSettings
    classifier_config: ClassifierSettings

class ExperimentConfig(Config):
    exp_name: str
    log_path: str
    save_path: str

    train_x_csv_path: str
    train_y_csv_path: str
    test_x_csv_path: str
    test_y_csv_path: str

class AppConfig(ExtraFieldsNotAllowedBaseModel):
    preprocessing_config: PreprocessorSettings
    load_path: str