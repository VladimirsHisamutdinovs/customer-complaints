"""
Customer Complaint Generator Agent module.
"""
import random
import ollama
import time
from kafka_queues.kafka_producer import KafkaProducerClient
from agents.base_agent import BaseAgent

class CustomerAgent(BaseAgent):
    def __init__(self, kafka_bootstrap_servers):
        self.producer = KafkaProducerClient(bootstrap_servers=kafka_bootstrap_servers)

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

    def send_test_messages(self):
        test_messages = [
            {"customer_id": "CUST1234", "location": "Region1", "complaint_text": "Internet down in my area!"},
            {"customer_id": "CUST5678", "location": "Region2", "complaint_text": "Slow speed during peak hours."},
            {"customer_id": "CUST9101", "location": "Region3", "complaint_text": "No connection for 2 days."}
        ]

        for message in test_messages:
            self.producer.send_message('customer_complaints', message)
            print(f"Sent: {message}")

        self.producer.flush()

    def run(self):
        while True:
            complaint = self.generate_complaint()
            self.producer.send_message('customer_complaints', complaint)
            print(f"Generated and sent complaint: {complaint}")
            time.sleep(10)  # Adjust sleep time as needed

if __name__ == "__main__":
    agent = CustomerAgent(kafka_bootstrap_servers='kafka:9092')
    agent.send_test_messages()
    agent.run()
