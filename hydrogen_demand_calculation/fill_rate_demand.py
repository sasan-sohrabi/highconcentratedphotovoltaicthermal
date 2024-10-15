import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define the mean (mu) and standard deviation (sigma) for the fill rate distribution
mu = 0.9  # Mean fill rate (kg/min)
sigma = 0.34  # Standard deviation (kg/min)

# Step 1: Generate random fill rates based on the normal distribution
# Generate 1000 random fill rates using the normal distribution
simulated_fill_rates = np.random.normal(mu, sigma, 1000)

# Step 2: Calculate the probability density for a specific fill rate (using the normal distribution formula)
z = .93  # Specific fill rate we want to calculate the probability for
probability_density = norm.pdf(z, mu, sigma)

# Output the probability density for fill rate z
print(f"Probability Density for fill rate {z} kg/min: {probability_density}")

# Step 3: Plot the histogram of the simulated fill rates and the probability density function
plt.hist(simulated_fill_rates, bins=30, density=True, alpha=0.6, color='g', label="Simulated Fill Rates")

# Plot the PDF (Probability Density Function) for the normal distribution
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, sigma)
plt.plot(x, p, 'k', linewidth=2, label="Normal Distribution PDF")
plt.title("Simulated Hydrogen Fill Rates")
plt.xlabel("Fill Rate (kg/min)")
plt.ylabel("Probability Density")
plt.legend()
plt.show()
