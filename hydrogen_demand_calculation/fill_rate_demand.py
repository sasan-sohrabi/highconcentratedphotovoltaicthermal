import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Step 1: Define the parameters of the normal distribution
mu = 0.9  # Mean fill rate (kg/min)
sigma = 0.1  # Standard deviation (kg/min)

# Step 2: Generate 1000 random fill rates based on the normal distribution
random_fill_rates = np.random.normal(mu, sigma, 1000)

# Step 3: Calculate the probability density for a specific fill rate (z = 1 kg/min)
z = 0.9  # Specific fill rate to calculate the probability for
probability = norm.pdf(z, mu, sigma)
print(f"Probability Density for fill rate {z} kg/min: {probability}")

# Step 4: Plot the histogram of the generated fill rates and the probability density function
plt.hist(random_fill_rates, bins=30, density=True, alpha=0.6, color='g')

# Plot the probability density function (PDF)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2)
plt.title("Probability Density of Hydrogen Fill Rates")
plt.xlabel("Fill Rate (kg/min)")
plt.ylabel("Probability Density")
plt.show()