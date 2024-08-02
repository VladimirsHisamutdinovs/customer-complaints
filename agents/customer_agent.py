"""
Customer Complaint Generator Agent module.
"""
import random
import ollama
from kafka.kafka_producer import KafkaProducerClient
from .base_agent import BaseAgent

class CustomerAgent(BaseAgent):
    def __init__(self, kafka_bootstrap_servers):
        self.kafka_producer = KafkaProducerClient(bootstrap_servers=kafka_bootstrap_servers)
        self.locations = ["Algeria", "Indonesia", "Iraq", "Kuwait", "Myanmar",
                          "Maldives", "Oman", "Palestine", "Qatar", "Tunisia"]
        self.likely_consequences = ["internet down", "slow speed", "no connection"]

    def generate_complaint(self):
        customer_id = f"CUST{random.randint(1000, 9999)}"
        location = random.choice(self.locations)
        consequence = random.choice(self.likely_consequences)
        complaint_text = self._generate_complaint_text(consequence)
        return {
            "customer_id": customer_id,
            "location": location,
            "complaint_text": complaint_text
        }

    def _generate_complaint_text(self, consequence):
        prompt = f"Generate a customer complaint based on the following issue: {consequence}."
        response = ollama.generate(prompt=prompt, model="phi3")
        return response['text']

    def run(self):
        while True:
            complaint = self.generate_complaint()
            self.kafka_producer.send_message('customer_complaints', complaint)
