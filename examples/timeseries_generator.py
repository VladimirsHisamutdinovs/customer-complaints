import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

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

# Function to simulate live data generation and plotting
def simulate_live_data_with_plot(generator, duration=60, interval=1):
    num_days = generator.num_days
    day = 0
    start_time = time.time()

    # Set up live plot
    plt.ion()
    fig, ax = plt.subplots(4, 1, figsize=(10, 8))
    fig.tight_layout(pad=3.0)
    
    network_load_line, = ax[0].plot([], [], label='Network Load', color='blue')
    throughput_line, = ax[1].plot([], [], label='Throughput', color='green')
    latency_line, = ax[2].plot([], [], label='Latency', color='red')
    user_count_line, = ax[3].plot([], [], label='User Count', color='purple')

    for axis in ax:
        axis.legend()
        axis.set_xlim(0, 365)  # Display all 52 weeks
        axis.set_ylim(0, 1200)

    while time.time() - start_time < duration:
        data = generator.generate_data(day)
        day += 1
        if day >= num_days:
            day = 0  # Reset day to cycle through the year again
        
        # Update plot data
        xdata = np.append(network_load_line.get_xdata(), data['time'])
        ydata_load = np.append(network_load_line.get_ydata(), data['network_load'])
        ydata_throughput = np.append(throughput_line.get_ydata(), data['throughput'])
        ydata_latency = np.append(latency_line.get_ydata(), data['latency'])
        ydata_user_count = np.append(user_count_line.get_ydata(), data['user_count'])

        network_load_line.set_data(xdata, ydata_load)
        throughput_line.set_data(xdata, ydata_throughput)
        latency_line.set_data(xdata, ydata_latency)
        user_count_line.set_data(xdata, ydata_user_count)

        for axis in ax:
            axis.relim()
            axis.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(interval)  # Simulate 1 second per simulated week

    plt.ioff()
    plt.show()

# Initialize generator
num_days = 365
generator = LiveNetworkTimeSeriesGenerator(num_days)

# Simulate live data generation with plotting
simulate_live_data_with_plot(generator, duration=60, interval=1)  # 1 second per simulated week
