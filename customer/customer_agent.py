"""
Customer Complaint Generator Agent module.
"""
import random
from ollama import Client
import time
from redis import Redis
from base_agent import BaseAgent

class CustomerAgent(BaseAgent):
    def __init__(self, redis_host):
        self.redis = Redis(host=redis_host, port=6379)
        self.ollama_client = Client(host='http://localhost:11434/')

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
        response = self.ollama_client.generate( model="phi3", prompt=prompt)
        return response['text']

    def run(self):
        while True:
            # Listen for manual initiation
            messages = self.redis.xread({'initiate_complaints': '0-0'}, block=0, count=1)
            if messages:
                stream, entries = messages[0]
                for entry_id, entry in entries:
                    print(f"Initiating complaint generation: {entry}")
                    complaint = self.generate_complaint()
                    self.redis.xadd('customer_complaints', complaint)
                    print(f"Generated and sent complaint: {complaint}")
                    self.redis.xack('initiate_complaints', stream, entry_id)

if __name__ == "__main__":
    agent = CustomerAgent(redis_host='redis')
    agent.run()
