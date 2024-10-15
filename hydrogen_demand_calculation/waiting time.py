import numpy as np

# Parameters
lambda_rate = 0.2  # Fill event rate (fills per minute)
wait_time = 5  # Specific waiting time in minutes

# Apply the formula P(W <= w) = lambda * exp(-lambda * w)
probability_density = lambda_rate * np.exp(-lambda_rate * wait_time)

# Output the result
print(f"Probability Density for waiting time of exactly {wait_time} minutes: {probability_density:.4f}")

# Calculate probability densities for different waiting times
waiting_times = [1, 3, 5, 7, 10]
probabilities = [lambda_rate * np.exp(-lambda_rate * w) for w in waiting_times]

# Display the results
for w, prob in zip(waiting_times, probabilities):
    print(f"Probability Density for waiting time of {w} minutes: {prob:.4f}")

