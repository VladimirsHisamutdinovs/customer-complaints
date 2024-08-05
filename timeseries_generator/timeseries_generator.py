import numpy as np
import pandas as pd
import time
import redis
from neo4j import GraphDatabase, basic_auth
import json
from datetime import datetime, timedelta
import os

# Initialize Redis connection
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port, db=0)

# Initialize Neo4j connection with retry mechanism
neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
neo4j_password = os.getenv('NEO4J_PASSWORD', 'password123')

driver = None
for _ in range(10):
    try:
        driver = GraphDatabase.driver(neo4j_uri, auth=basic_auth(neo4j_user, neo4j_password))
        driver.verify_connectivity()
        print("Connected to Neo4j")
        break
    except Exception as e:
        print(f"Neo4j connection failed: {e}, retrying...")
        time.sleep(5)

if driver is None:
    raise Exception("Failed to connect to Neo4j after multiple attempts")

class LiveNetworkTimeSeriesGenerator:
    def __init__(self, num_intervals, start_time):
        self.num_intervals = num_intervals
        self.time = np.arange(num_intervals)
        self.start_time = start_time
        self.daily_cycle = self.generate_daily_cycle()
        self.weekly_cycle = self.generate_weekly_cycle()
        self.seasonal_cycle = self.generate_seasonal_cycle()
        self.random_outliers = self.generate_random_outliers()
        self.weather_impact = self.generate_weather_impact()
        self.user_count_base = 1000

    def generate_daily_cycle(self):
        return 30 * np.sin(self.time * 2 * np.pi / (24 * 4))  # 96 intervals in a day

    def generate_weekly_cycle(self):
        return 60 * np.sin(self.time * 2 * np.pi / (7 * 24 * 4))  # 672 intervals in a week

    def generate_seasonal_cycle(self):
        seasonal_cycle = np.ones(self.num_intervals)
        num_days = self.num_intervals // (24 * 4)
        seasonal_cycle[150*4:243*4] *= 0.3  # Decrease usage in June, July, August
        return seasonal_cycle

    def generate_random_outliers(self):
        outliers = np.zeros(self.num_intervals)
        outliers[np.random.randint(0, self.num_intervals, 10)] = -150  # Random faults
        return outliers

    def generate_weather_impact(self):
        weather = np.random.normal(0, 20, self.num_intervals)  # Random weather impact
        return weather

    def generate_network_load(self, interval):
        base_load = 100 * self.seasonal_cycle[interval % self.num_intervals]
        load = (base_load +
                self.daily_cycle[interval % (24 * 4)] +
                self.weekly_cycle[interval % (7 * 24 * 4)] +
                self.random_outliers[interval % self.num_intervals] +
                self.weather_impact[interval % self.num_intervals])

        # Adjust for customer activity patterns
        if (interval % (24 * 4)) in range(32, 80):  # Evening
            load *= 1.4
        elif (interval % (24 * 4)) in range(80, 96) or (interval % (24 * 4)) in range(0, 16):  # Night
            load *= 0.3
        elif (interval % (7 * 24 * 4)) in range(5 * 24 * 4, 7 * 24 * 4):  # Weekend
            load *= 1.4

        return load

    def generate_user_count(self, interval):
        user_count = self.user_count_base + (interval // (24 * 4))  # Increase by 1 user per day
        return user_count

    def generate_data(self, interval):
        network_load = round(self.generate_network_load(interval), 2)
        throughput = round(200 - network_load, 2)  # Inverse relation for simplicity
        latency = round(100 + (network_load / 1.5), 2)  # Higher load, higher latency
        user_count = self.generate_user_count(interval)  # User count with delay effects
        timestamp = self.start_time + timedelta(minutes=15*interval)

        data = {
            'time': timestamp.isoformat(),
            'network_load': network_load,
            'throughput': throughput,
            'latency': latency,
            'user_count': user_count
        }
        print(f"Generated data for interval {interval}: {data}")  # Log generated data
        return data

    def push_to_redis(self, data):
        r.rpush('timeseries_data', json.dumps(data))
        print(f"Pushed to Redis: {data}")  # Log data pushed to Redis

    def store_in_neo4j(self, data):
        with driver.session() as session:
            session.execute_write(self._store_data, data)
            print(f"Stored in Neo4j: {data}")  # Log data stored in Neo4j

    @staticmethod
    def _store_data(tx, data):
        query = """
        MERGE (t:TimeSeries {time: $time})
        SET t.network_load = $network_load,
            t.throughput = $throughput,
            t.latency = $latency,
            t.user_count = $user_count
        """
        tx.run(query, data)

def generate_and_process_data(generator, duration=365*24*4, interval=1):
    interval_counter = 0
    high_load_days = np.random.choice(range(duration // (24 * 4)), size=52, replace=False)  # 2 high load events per week
    critical_load_days = np.random.choice(range(duration // (24 * 4)), size=26, replace=False)  # 1 critical load event per 2 weeks

    while interval_counter < duration:
        data = generator.generate_data(interval_counter)

        # Simulate high loads
        if (interval_counter // (24 * 4)) in high_load_days:
            if interval_counter % (24 * 4) in range(32, 80) or (interval_counter % (7 * 24 * 4)) in range(5 * 24 * 4, 7 * 24 * 4):
                data['network_load'] *= 1.5

        # Simulate critical loads
        if (interval_counter // (24 * 4)) in critical_load_days:
            if interval_counter % (24 * 4) in range(0, 96):
                data['network_load'] *= 2

        generator.push_to_redis(data)
        generator.store_in_neo4j(data)
        print(f"Data generated for interval {interval_counter}: {data}")
        interval_counter += 1
        time.sleep(interval)  # Simulate 1 second per 15 minutes

if __name__ == '__main__':
    num_intervals = 365 * 24 * 4
    start_time = datetime(2024, 1, 1)
    generator = LiveNetworkTimeSeriesGenerator(num_intervals, start_time)
    generate_and_process_data(generator, duration=num_intervals, interval=1)  # 1 second per simulated 15 minutes
