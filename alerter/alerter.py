from redis import Redis
import time
import json

# Initialize Redis connection
redis_host = 'redis'
redis_port = 6379
r = Redis(host=redis_host, port=redis_port, db=0)

ALERT_QUEUE = 'alerts'

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
        self.previous_alerts = {'network_load': 0, 'throughput': 0, 'latency': 0, 'user_count': 0}
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
        current_day = data['time']
        
        for key, value in data.items():
            if key != 'time':
                if key == 'user_count':
                    if value < self.user_count_base * self.alert_thresholds[key]['actionable']:
                        alerts.append((current_day, key, 'actionable'))
                    elif value > self.user_count_base * self.alert_thresholds[key]['critical']:
                        alerts.append((current_day, key, 'critical'))
                else:
                    if value > self.alert_thresholds[key]['critical']:
                        alerts.append((current_day, key, 'critical'))
                    elif value > self.alert_thresholds[key]['actionable']:
                        alerts.append((current_day, key, 'actionable'))

        return alerts

    def trigger_alerts(self, alerts):
        for alert in alerts:
            day, reason, level = alert
            if self.previous_alerts[reason] + self.delay_days <= day:
                # Trigger alert and update the previous alert day
                self.previous_alerts[reason] = day
                self.send_alert_to_redis(day, reason, level)
    
    def send_alert_to_redis(self, day, reason, level):
        consequence = self.consequence_mapping[reason][level]
        alert_message = f"Day: {day}, Reason: {reason}, Level: {level}, Consequence: {consequence}"
        r.rpush(ALERT_QUEUE, alert_message)
        print(f"Alert triggered: {alert_message}")

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
