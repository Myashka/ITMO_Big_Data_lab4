import json
import os

from kafka import KafkaConsumer

from src.classifier import Classifier
from src.db import models
from src.db.database import Database
from src.preprocessor import Preprocessor
from src.settings.config import AppConfig
from src.settings.preprocessor import PreprocessorSettings
from src.utils import load_config

# Загрузка конфигурации
config: AppConfig = load_config()
assert os.path.isdir(config.load_path), "There is no model dir"
preprocessor_settings = PreprocessorSettings(**config.preprocessing_config.dict())
preprocessor = Preprocessor(settings=preprocessor_settings)
classifier = Classifier.load(config.load_path)

# Инициализация базы данных
db = Database(os.getenv("DATABASE_URL"))
topic_name = os.getenv("KAFKA_TOPIC_NAME", "classify-topic")

# Kafka консьюмер
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def handle_message(message: str, db: Database):
    session = next(db.get_db())
    try:
        processed_text = preprocessor.preprocess(message)
        pred = classifier.predict(processed_text)
        
        result = models.Result(message=message, sentiment=pred.sentiment)
        session.add(result)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    for msg in consumer:
        handle_message(msg.value['message'], db)

if __name__ == "__main__":
    main()
