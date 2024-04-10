from configparser import ConfigParser

import pandas as pd
import yaml
from pydantic import ValidationError

from src.settings.config import AppConfig, ExperimentConfig
from src.settings.preprocessor import PreprocessorSettings


def load_experiment_config(config_path: str) -> ExperimentConfig:
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)
    try:
        config = ExperimentConfig(**config_data)
        return config
    except ValidationError as e:
        print(f"Ошибка валидации конфигурации: {e}")
        raise

def read_exp_data(config: ExperimentConfig):
    train_x = pd.read_csv(config.train_x_csv_path)
    train_y = pd.read_csv(config.train_y_csv_path).squeeze()
    test_x = pd.read_csv(config.test_x_csv_path)
    test_y = pd.read_csv(config.test_y_csv_path).squeeze()
    return train_x, train_y, test_x, test_y

def load_config(config_path: str = "config.ini") -> AppConfig:
    config = ConfigParser()
    config.read(config_path)

    preprocessing_config = PreprocessorSettings(
        use_normalization=config.getboolean("preprocessing", "use_normalization"),
        use_lemmatization=config.getboolean("preprocessing", "use_lemmatization")
    )

    load_path = config.get("paths", "load_path")

    return AppConfig(
        preprocessing_config=preprocessing_config,
        load_path=load_path
    )