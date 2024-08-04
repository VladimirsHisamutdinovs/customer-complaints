import redis
import time

# Initialize Redis connection
redis_host = 'redis'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0)

class Alerter:
    def __init__(self):
        self.alert_thresholds = {
            'network_load': {'actionable': 70, 'critical': 90},
            'throughput': {'actionable': 60, 'critical': 40},
            'latency': {'actionable': 200, 'critical': 300}
        }
        self.previous_alerts = {'network_load': 0, 'throughput': 0, 'latency': 0}
        self.delay_days = 3

    def check_thresholds(self, data):
        alerts = []
        current_day = data['time']
        
        for key, value in data.items():
            if key != 'time':
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
        alert_message = f"Day: {day}, Reason: {reason}, Level: {level}"
        r.rpush('alerts', alert_message)
        print(f"Alert triggered: {alert_message}")

def process_alerts():
    alerter = Alerter()
    while True:
        if r.llen('timeseries_data') > 0:
            data = r.lpop('timeseries_data')
            data = eval(data)  # Convert the string back to dictionary
            alerts = alerter.check_thresholds(data)
            alerter.trigger_alerts(alerts)
        time.sleep(1)  # Check for new data every second

if __name__ == '__main__':
    process_alerts()
