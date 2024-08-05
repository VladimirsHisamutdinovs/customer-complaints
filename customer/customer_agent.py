import random
from ollama import Client
import time
from redis import Redis
from base_agent import BaseAgent

ALERT_QUEUE = 'alerts'
COMPLAINT_QUEUE = 'customer_complaints'

class CustomerAgent(BaseAgent):
    def __init__(self, redis_host='redis', redis_port=6379):
        super().__init__(redis_host, redis_port)
        self.redis = Redis(host=self.redis_host, port=self.redis_port)
        self.ollama_client = Client(host='http://localhost:11434/')

    def generate_complaint(self, alert):
        customer_id = f"CUST{random.randint(1000, 9999)}"
        complaint_text = self._generate_complaint_text(alert)
        return {
            "customer_id": customer_id,
            "complaint_text": complaint_text
        }

    def _generate_complaint_text(self, alert):
        # Extract alert details
        day, reason, level, consequence = self._parse_alert(alert)
        prompt = f"Generate a customer complaint based on the following issue on day {day}: {consequence}."
        response = self.ollama_client.generate(model="phi3", prompt=prompt)
        print(response)
        return response['text']

    def _parse_alert(self, alert):
        # Parse alert message format: "Day: {day}, Reason: {reason}, Level: {level}, Consequence: {consequence}"
        parts = alert.split(', ')
        alert_data = {part.split(': ')[0]: part.split(': ')[1] for part in parts}
        return alert_data['Day'], alert_data['Reason'], alert_data['Level'], alert_data['Consequence']

    def run(self):
        while True:
            # Listen for alerts
            if self.redis.llen(ALERT_QUEUE) > 0:
                alert = self.redis.lpop(ALERT_QUEUE).decode('utf-8')
                print(f"Received alert: {alert}")
                complaint = self.generate_complaint(alert)
                # Convert complaint dictionary to the format accepted by Redis Streams
                complaint_redis_format = {k: str(v) for k, v in complaint.items()}
                self.redis.xadd(COMPLAINT_QUEUE, complaint_redis_format)
                print(f"Generated and sent complaint: {complaint}")
            time.sleep(1)  # Check for new alerts every second

if __name__ == "__main__":
    agent = CustomerAgent(redis_host='redis')
    agent.run()
