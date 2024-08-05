import numpy as np
import pandas as pd
import time
import redis
import psycopg2
import timesfm
import json

# Initialize Redis connection
redis_host = 'redis'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0)

# Initialize PostgreSQL connection
conn = psycopg2.connect(
    dbname="your_dbname",
    user="your_user",
    password="your_password",
    host="postgres"
)
cur = conn.cursor()

class LiveNetworkTimeSeriesGenerator:
    def __init__(self, num_days):
        self.num_days = num_days
        self.time = np.arange(num_days)
        self.daily_cycle = self.generate_daily_cycle()
        self.weekly_cycle = self.generate_weekly_cycle()
        self.seasonal_cycle = self.generate_seasonal_cycle()
        self.maintenance_events = self.generate_maintenance_events()
        self.marketing_campaigns = self.generate_marketing_campaigns()
        self.random_outliers = self.generate_random_outliers()
        self.weather_impact = self.generate_weather_impact()
        self.user_count_base = 1000
        self.model = timesfm.TimesFM()  # Initialize the TimesFM model

    def generate_daily_cycle(self):
        return 30 * np.sin(self.time * 2 * np.pi / 24)
    
    def generate_weekly_cycle(self):
        return 60 * np.sin(self.time * 2 * np.pi / 168)
    
    def generate_seasonal_cycle(self):
        seasonal_cycle = np.ones(self.num_days)
        seasonal_cycle[150:243] *= 0.3  # Decrease usage in June, July, August
        return seasonal_cycle
    
    def generate_maintenance_events(self):
        maintenance = np.zeros(self.num_days)
        maintenance[::30] = -70  # Scheduled maintenance every month
        return maintenance
    
    def generate_marketing_campaigns(self):
        marketing = np.zeros(self.num_days)
        marketing[::90] = 50  # Marketing campaigns every three months (5% increase)
        return marketing
    
    def generate_random_outliers(self):
        outliers = np.zeros(self.num_days)
        outliers[np.random.randint(0, self.num_days, 10)] = -150  # Random faults
        return outliers
    
    def generate_weather_impact(self):
        weather = np.random.normal(0, 20, self.num_days)  # Random weather impact
        return weather

    def generate_network_load(self, day):
        base_load = 100 * self.seasonal_cycle[day % self.num_days]
        load = (base_load + 
                self.daily_cycle[day % 24] + 
                self.weekly_cycle[day % 168] + 
                self.maintenance_events[day % self.num_days] + 
                self.marketing_campaigns[day % self.num_days] + 
                self.random_outliers[day % self.num_days] + 
                self.weather_impact[day % self.num_days])
        return load

    def generate_user_count(self, day):
        user_count = self.user_count_base
        # Apply marketing campaign with delay
        for delay in range(1, 4):
            if day - delay >= 0 and self.marketing_campaigns[(day - delay) % self.num_days] > 0:
                user_count += self.user_count_base * 0.1  # Increase by 10%
        # Apply fault impact with delay
        for delay in range(1, 4):
            if day - delay >= 0 and self.random_outliers[(day - delay) % self.num_days] < 0:
                user_count -= self.user_count_base * 0.1  # Decrease by 10%
        return user_count

    def generate_data(self, day):
        network_load = self.generate_network_load(day)
        throughput = 200 - network_load  # Inverse relation for simplicity
        latency = 100 + (network_load / 1.5)  # Higher load, higher latency
        user_count = self.generate_user_count(day)  # User count with delay effects
        
        data = {
            'time': day,
            'network_load': network_load,
            'throughput': throughput,
            'latency': latency,
            'user_count': user_count
        }
        return data

    def push_to_redis(self, data):
        r.rpush('timeseries_data', json.dumps(data))

    def store_in_postgres(self, data):
        cur.execute(
            """
            INSERT INTO timeseries_data (time, network_load, throughput, latency, user_count)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['time'], data['network_load'], data['throughput'], data['latency'], data['user_count'])
        )
        conn.commit()

    def feed_to_model(self, data):
        # Assuming the model expects data in a certain format
        features = [[data['network_load'], data['throughput'], data['latency'], data['user_count']]]
        self.model.predict(features)

def generate_and_process_data(generator, duration=365, interval=1):
    day = 0
    while day < duration:
        data = generator.generate_data(day)
        generator.push_to_redis(data)
        generator.store_in_postgres(data)
        generator.feed_to_model(data)
        print(f"Data generated for day {day}: {data}")
        day += 1
        time.sleep(interval)  # Simulate 1 second per day

if __name__ == '__main__':
    num_days = 365
    generator = LiveNetworkTimeSeriesGenerator(num_days)
    generate_and_process_data(generator, duration=num_days, interval=1)  # 1 second per simulated day
