from redis import Redis
import time
import json
import random
from datetime import datetime, timedelta

# Initialize Redis connection
redis_host = 'redis'
redis_port = 6379
r = Redis(host=redis_host, port=redis_port, db=0)

ALERT_QUEUE = 'alerts'
COMPLAINTS_QUEUE = 'complaints'

class Alerter:
    def __init__(self):
        self.redis = Redis(host=redis_host, port=redis_port)
        self.user_count_base = 1000  # Define the base user count
        self.alert_thresholds = {
            'network_load': {'actionable': 70, 'critical': 90},
            'throughput': {'actionable': 60, 'critical': 40},
            'latency': {'actionable': 200, 'critical': 300},
            'user_count': {'actionable': 0.1, 'critical': 0.9}
        }
        self.previous_alerts = {
            'network_load': datetime.min,
            'throughput': datetime.min,
            'latency': datetime.min,
            'user_count': datetime.min
        }
        self.delay_days = 3
        self.consequence_mapping = {
            'network_load': {
                'actionable': "Customers may experience slow internet speeds.",
                'critical': "Customers are experiencing very slow internet speeds and buffering issues."
            },
            'throughput': {
                'actionable': "Customers may experience slow download and upload speeds.",
                'critical': "Customers are experiencing very slow download and upload speeds, impacting streaming and online activities."
            },
            'latency': {
                'actionable': "Customers may experience lag in online activities such as gaming and video calls.",
                'critical': "Customers are experiencing significant lag in online activities, causing disruptions in gaming and video calls."
            },
            'user_count': {
                'actionable': "The number of users is unusually low.",
                'critical': "The number of users is critically low, indicating a potential service outage."
            }
        }

    def check_thresholds(self, data):
        alerts = []
        current_time = datetime.fromisoformat(data['time'])
        
        for key, value in data.items():
            if key != 'time':
                if key == 'user_count':
                    if value < self.user_count_base * self.alert_thresholds[key]['actionable']:
                        alerts.append((current_time, key, 'actionable'))
                    elif value > self.user_count_base * self.alert_thresholds[key]['critical']:
                        alerts.append((current_time, key, 'critical'))
                else:
                    if value > self.alert_thresholds[key]['critical']:
                        alerts.append((current_time, key, 'critical'))
                    elif value > self.alert_thresholds[key]['actionable']:
                        alerts.append((current_time, key, 'actionable'))

        return alerts

    def trigger_alerts(self, alerts):
        for alert in alerts:
            time, reason, level = alert
            if self.previous_alerts[reason] + timedelta(days=self.delay_days) <= time:
                # Trigger alert and update the previous alert time
                self.previous_alerts[reason] = time
                self.send_alert_to_redis(time, reason, level)
    
    def send_alert_to_redis(self, time, reason, level):
        consequence = self.consequence_mapping[reason][level]
        alert_message = {
            'time': (time + timedelta(hours=1)).isoformat(),
            'reason': reason,
            'level': level,
            'consequence': consequence
        }
        r.rpush(ALERT_QUEUE, json.dumps(alert_message))
        print(f"Alert triggered: {alert_message}")  # Print alert to console
        
        # Generate complaints
        num_complaints = self.generate_complaints(alert_message, level)
        for complaint in num_complaints:
            r.rpush(COMPLAINTS_QUEUE, json.dumps(complaint))
            print(f"Complaint generated: {complaint}")  # Print complaint to console

    def generate_complaints(self, alert_message, level):
        complaints = []
        num_users = self.user_count_base
        if level == 'actionable':
            num_complaints = int(num_users * 0.05)
        else:
            num_complaints = int(num_users * 0.25)
        
        for _ in range(num_complaints):
            area = random.randint(1, 10)
            complaint = {
                'time': alert_message['time'],
                'area': area,
                'complaint': alert_message['consequence']
            }
            complaints.append(complaint)
        
        return complaints

def process_alerts():
    alerter = Alerter()
    while True:
        if r.llen('timeseries_data') > 0:
            data = r.lpop('timeseries_data')
            data = json.loads(data)  # Convert the JSON string back to dictionary
            alerts = alerter.check_thresholds(data)
            alerter.trigger_alerts(alerts)
        time.sleep(1)  # Check for new data every second

if __name__ == '__main__':
    process_alerts()
