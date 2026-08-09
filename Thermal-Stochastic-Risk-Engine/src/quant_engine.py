import numpy as np
import pandas as pd

# Making a Stotchastic Risk Engine class to simulate GBM stock paths
class StochasticRiskEngine:

    # Making values for the number of simulations and time steps
    def __init__(self, num_simulations=1000, time_steps=252):
        self.num_simulations = num_simulations
        self.time_steps = time_steps

    # Setting up the GBM stock path simulation by creating variables for the initial stock price, expected return, volatility, and time increment
    def simulate_gbm_stock_paths(self, s0=100, mu=0.07, sigma=0.13, dt=1/252):

        # Creating an array to hold the simulated stock paths. The first stock is our intital stock price.
        paths = np.zeros((self.time_steps, self.num_simulations))
        paths[0] = s0

        # Creating the variable z which represents N(0,1) in our equation
        z = np.random.normal(loc=0, scale=1, size=(self.time_steps - 1, self.num_simulations))

        # Using the GBM formula to simulate the stock paths over time
        for t in range(1, self.time_steps):
            paths[t] = paths[t - 1] * np.exp(
                (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z[t - 1]
            )

        return paths

    # Calculating the probability of thermal failure based on the simulated thermal paths and the maximum safe limit
    def calculate_thermal_failure_probability(self, thermal_paths, max_safe_limit):

        # Checking if any temperatures exceed the maximum safe limit
        exceeded_limit = np.any(thermal_paths >= max_safe_limit, axis=0)

        # Calculating the probability of failure by taking the mean of the array
        failure_probability = np.mean(exceeded_limit)
        return failure_probability

# Testing the StochasticRiskEngine class and the outputs
if __name__ == "__main__":
    engine = StochasticRiskEngine(num_simulations=1000, time_steps=252)

    # Simulate GBM stock paths and print the shape and mean of the final stock prices
    stock_paths = engine.simulate_gbm_stock_paths(s0=100, mu=0.07, sigma=0.13)
    print("Stock Path Simulation Shape:", stock_paths.shape)
    print("Final Simulated Stock Price Mean: $", np.mean(stock_paths[-1]))

    # Simulate thermal paths and calculate the probability of exceeding the maximum safe limit
    mock_thermal_paths = np.random.normal(loc=60, scale=4, size=(252, 1000))
    fail_prob = engine.calculate_thermal_failure_probability(mock_thermal_paths, max_safe_limit=90)
    print(f"Calculated Thermal Failure Probability: {fail_prob * 100:.2f}%")