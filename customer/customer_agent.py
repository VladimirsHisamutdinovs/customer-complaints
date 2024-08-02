"""
Customer Complaint Generator Agent module.
"""
import random
import ollama
import time
from kafka_queues.kafka_producer import KafkaProducerClient
from utils.base_agent import BaseAgent

class CustomerAgent(BaseAgent):
    def __init__(self, kafka_bootstrap_servers):
        self.producer = KafkaProducerClient(bootstrap_servers=kafka_bootstrap_servers)

    def generate_complaint(self):
        customer_id = f"CUST{random.randint(1000, 9999)}"
        complaint_text = self._generate_complaint_text()
        return {
            "customer_id": customer_id,
            "complaint_text": complaint_text
        }

    def _generate_complaint_text(self):
        consequences = ["internet down", "slow speed", "no connection"]
        consequence = random.choice(consequences)
        prompt = f"Generate a customer complaint based on the following issue: {consequence}."
        response = ollama.generate(prompt=prompt, model="phi3", server_url="http://customer_ollama:11434")
        return response['text']

    def run(self):
        while True:
            complaint = self.generate_complaint()
            self.producer.send_message('customer_complaints', complaint)
            print(f"Generated and sent complaint: {complaint}")
            time.sleep(10)  # Adjust sleep time as needed

if __name__ == "__main__":
    agent = CustomerAgent(kafka_bootstrap_servers='kafka:9092')
    agent.run()
