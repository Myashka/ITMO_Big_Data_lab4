import json
import os

from sqlalchemy.exc import SQLAlchemyError

from kafka import KafkaConsumer
from src.classifier import Classifier
from src.db import models
from src.db.database import Database
from src.preprocessor import Preprocessor
from src.settings.config import AppConfig
from src.settings.preprocessor import PreprocessorSettings
from src.utils import load_config


class KafkaClassifierConsumer:
    def __init__(self):
        self.config: AppConfig = load_config()
        assert os.path.isdir(self.config.load_path), "Model directory does not exist"
        
        self.preprocessor_settings = PreprocessorSettings(**self.config.preprocessing_config.dict())
        self.preprocessor = Preprocessor(settings=self.preprocessor_settings)
        self.classifier = Classifier.load(self.config.load_path)
        
        self.db = Database(os.getenv("DATABASE_URL"))
        self.consumer = KafkaConsumer(
            os.getenv("KAFKA_TOPIC_NAME", "classify-topic"),
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def handle_message(self, message: str):
        session = next(self.db.get_db())
        try:
            processed_text = self.preprocessor.preprocess(message)
            pred = self.classifier.predict(processed_text)
            result = models.Result(message=message, sentiment=pred.sentiment)
            session.add(result)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        finally:
            session.close()
    
    def run(self):
        for msg in self.consumer:
            self.handle_message(msg.value['message'])

if __name__ == "__main__":
    consumer = KafkaClassifierConsumer()
    consumer.run()