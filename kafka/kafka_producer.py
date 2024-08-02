"""
Kafka Producer module to send messages to Kafka topics.
"""
from kafka import KafkaProducer
import json

class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        self.producer.send(topic, value=message)
        self.producer.flush()
