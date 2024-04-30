import json

from kafka import KafkaProducer


class KafkaProducerManager:
    def __init__(self, servers):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        self.producer.send(topic, value={'message': message})
        self.producer.flush()  # Ensure all messages are sent

    def close(self):
        self.producer.close()
