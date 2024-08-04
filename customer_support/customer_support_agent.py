"""
Customer Support Agent module.
"""
import ollama
import logging
from redis import Redis
from neo4j_graphdb.neo4j_client import Neo4jClient
from postgres.postgres_client import PostgresClient
from base_agent import BaseAgent

logging.basicConfig(level=logging.INFO)

class CustomerSupportAgent(BaseAgent):
    def __init__(self, redis_host, neo4j_config, postgres_config, ollama_url):
        self.redis = Redis(host=redis_host, port=6379)
        self.neo4j_client = Neo4jClient(**neo4j_config)
        self.postgres_client = PostgresClient(**postgres_config)
        self.ollama_client = ollama.Client(host='http://localhost:11434')
        self.ollama_client.base_url = ollama_url

# TODO: put complaint on the resolver queue
    def process_complaint(self, complaint):
        logging.info(f"Processing complaint: {complaint}")
        self._store_complaint(complaint)
        return 

    def _store_complaint(self, complaint):
        self.neo4j_client.store_complaint(complaint)
        self.postgres_client.store_technical_complaint(complaint)

    def run(self):
        while True:
            complaints = self.redis.xread({'customer_complaints': '0-0'}, block=0, count=1)
            if complaints:
                stream, messages = complaints[0]
                for message_id, complaint in messages:
                    logging.info(f"Received complaint: {complaint}")
                    self.redis.xadd('technical_complaints', complaint)  # Always add to technical complaints stream
                    self.redis.xack('customer_complaints', stream, message_id)

if __name__ == "__main__":
    agent = CustomerSupportAgent(
        redis_host='redis',
        neo4j_config={
            "uri": "bolt://neo4j:7687",
            "user": "neo4j",
            "password": "password"
        },
        postgres_config={
            "dbname": "complaints_db",
            "user": "user",
            "password": "password",
            "host": "postgres"
        },
        ollama_url="http://support_ollama:11434"
    )
    agent.run()
