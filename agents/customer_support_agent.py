"""
Customer Support Agent module.
"""
import ollama
import logging
from kafka_queues.kafka_consumer import KafkaConsumerClient
from kafka_queues.kafka_producer import KafkaProducerClient
from neo4j_graphdb.neo4j_client import Neo4jClient
from postgres.postgres_client import PostgresClient
from agents.base_agent import BaseAgent

logging.basicConfig(level=logging.INFO)

class CustomerSupportAgent(BaseAgent):
    def __init__(self, kafka_bootstrap_servers, neo4j_config, postgres_config):
        self.consumer = KafkaConsumerClient(topic='customer_complaints', bootstrap_servers=kafka_bootstrap_servers)
        self.producer = KafkaProducerClient(bootstrap_servers=kafka_bootstrap_servers)
        self.neo4j_client = Neo4jClient(**neo4j_config)
        self.postgres_client = PostgresClient(**postgres_config)

    def process_complaint(self, complaint):
        logging.info(f"Processing complaint: {complaint}")
        category = self._classify_complaint(complaint["complaint_text"])
        self._store_complaint(complaint, category)
        return category

    def _classify_complaint(self, complaint_text):
        prompt = f"Classify the following complaint: {complaint_text}."
        response = ollama.generate(prompt=prompt, model="phi3", server_url="http://ollama:11434")

        return 'financial' if 'financial' in response['text'].lower() else 'technical'

    def _store_complaint(self, complaint, category):
        self.neo4j_client.store_complaint(complaint)
        if category == 'financial':
            self.postgres_client.store_financial_complaint(complaint)
        else:
            self.postgres_client.store_technical_complaint(complaint)

    def run(self):
        def process_message(complaint):
            logging.info(f"Received complaint: {complaint}")
            category = self.process_complaint(complaint)
            if category == 'financial':
                self.producer.send_message('financial_complaints', complaint)
            else:
                self.producer.send_message('technical_complaints', complaint)

        self.consumer.consume_messages(process_message)
