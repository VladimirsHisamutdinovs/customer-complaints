"""
Kafka Consumer module to consume messages from Kafka topics.
"""
from kafka import KafkaConsumer
import json

class KafkaConsumerClient:
    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_messages(self, callback):
        for message in self.consumer:
            callback(message.value)
