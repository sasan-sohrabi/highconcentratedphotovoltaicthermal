import numpy as np
import matplotlib.pyplot as plt

# Parameters
hours_per_day = 24
days_per_year = 365
total_hours = hours_per_day * days_per_year
weekly_demand = 5000  # in kg
avg_fill_amount = 3.5  # in kg
fill_rate = 1  # kg/min
hours_per_week = 168
lambda_per_hour = weekly_demand / (hours_per_week * avg_fill_amount)  # Avg fills per hour

# Poisson process: Number of fills per hour
hourly_fills = np.random.poisson(lambda_per_hour, total_hours)

# Generate random fill amounts (normally distributed)
fill_amounts = np.random.normal(avg_fill_amount, 0.5, sum(hourly_fills))

# Generate total hydrogen demand per hour
hydrogen_demand = []
fill_idx = 0
for fills in hourly_fills:
    total_demand = sum(fill_amounts[fill_idx:fill_idx+fills])
    hydrogen_demand.append(total_demand)
    fill_idx += fills

# Plot the total hydrogen demand over the year
plt.plot(hydrogen_demand)
plt.title('Simulated Hydrogen Demand for 8760 Hours')
plt.xlabel('Hours')
plt.ylabel('Total Hydrogen Demand (kg)')
plt.show()
