import json
import os
import sys

from loguru import logger
from sklearn.metrics import classification_report

from src.classifier import Classifier
from src.preprocessor import Preprocessor
from src.settings.classifier import PredictOutput
from src.settings.config import ExperimentConfig
from src.utils import load_experiment_config, read_exp_data


def setup_logger(config: ExperimentConfig):
    log_path = os.path.join(config.log_path, f"{config.exp_name}.log")
    os.makedirs(config.log_path, exist_ok=True)
    logger.add(log_path, level="INFO")

def run_experiment(config_path: str):
    config: ExperimentConfig = load_experiment_config(config_path)
    setup_logger(config)

    logger.info("Запуск эксперимента: {}", config.exp_name)
    logger.info(f"Конфигурация эксперимента:\n{json.dumps(config.dict(), indent=4, ensure_ascii=False)}")

    preprocessor = Preprocessor(config.preprocessing_config)
    classifier = Classifier(config.classifier_config)
    train_x, train_y, test_x, test_y = read_exp_data(config)

    train_x_processed = train_x['text'].apply(preprocessor.preprocess)
    classifier.fit(train_x_processed, train_y)

    test_x_processed = test_x['text'].apply(preprocessor.preprocess)
    pred: PredictOutput = classifier.predict(test_x_processed)

    text_test_y = [config.classifier_config.id2label[id] for id in test_y]

    report = classification_report(text_test_y, pred.sentiment, target_names=list(config.classifier_config.id2label.values()))

    logger.info("Classification Report:\n{}", report)

    classifier.save(config.save_path)
    logger.info("Модель сохранена в: {}", config.save_path)
    logger.info("Векторизатор сохранен в: {}", config.save_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python run_exp.py <путь_к_конфигу>")
        sys.exit(1)
    config_path = sys.argv[1]
    run_experiment(config_path)
