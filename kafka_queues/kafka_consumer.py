from kafka import KafkaConsumer
import json

class KafkaConsumerClient:
    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_messages(self):
        for message in self.consumer:
            print(f"Received message: {message.value}")

if __name__ == "__main__":
    consumer = KafkaConsumerClient(topic='some_topic', bootstrap_servers='kafka:9092')
    consumer.consume_messages()
