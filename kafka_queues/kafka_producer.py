import time
from kafka import KafkaProducer
import json

class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()

if __name__ == "__main__":
    producer = KafkaProducerClient(bootstrap_servers='kafka:9092')
    while True:
        message = {"key": "value"}
        producer.send_message('some_topic', message)
        print(f"Sent message: {message}")
        time.sleep(5)  # Adjust the sleep time as needed
