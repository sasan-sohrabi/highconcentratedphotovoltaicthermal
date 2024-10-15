import numpy as np
from scipy.stats import gaussian_kde, ks_2samp
import pandas as pd
import matplotlib.pyplot as plt

# Set a seed for reproducibility
np.random.seed(42)

# Real data provided
real_data = [2, 3, 3.4, 3.6, 4, 4.2, 5]

# Step 1: Perform Kernel Density Estimation (KDE) for the real data
kde_real = gaussian_kde(real_data)

# Step 2: Generate uniform random samples (using the fixed seed)
uniform_random_samples = np.random.uniform(0, 1, len(real_data))

# Step 3: Create a range of values for KDE evaluation and calculate the CDF
x_range = np.linspace(min(real_data) - 1, max(real_data) + 1, 7)
cdf_real = np.cumsum(kde_real(x_range))

# Normalize the CDF to be between 0 and 1
cdf_real /= cdf_real[-1]

# Step 4: Use inverse transform sampling to map the uniform samples to the KDE-based fill amounts
simulated_data_kde = np.interp(uniform_random_samples, cdf_real, x_range)

# Step 5: Perform Kolmogorov-Smirnov (KS) test to compare real and simulated data
statistic, p_value = ks_2samp(real_data, simulated_data_kde)

# Step 6: Prepare the comparison data
comparison_kde = pd.DataFrame({
    'Real Data': real_data,
    'Simulated Data (KDE)': simulated_data_kde
})

# Output the comparison and KS test results
print(comparison_kde)
print("KS Statistic:", statistic)
print("P-Value:", p_value)

# Optional: Plot the real vs simulated data
plt.hist(real_data, bins=10, alpha=0.5, label="Real Data")
plt.hist(simulated_data_kde, bins=10, alpha=0.5, label="Simulated Data (KDE)")
plt.legend()
plt.title("Real vs Simulated Data")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.show()
