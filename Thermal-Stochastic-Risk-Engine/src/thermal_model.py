import numpy as np
import pandas as pd

# Making a thermal cooling loop simulation class to create sensor data
class ThermalCoolingLoop:

    # Making values for ambient temperature and the max safe temperature
    def __init__(self, ambient_temp=20, max_safe_temp=90):
        self.ambient_temp = ambient_temp
        self.max_safe_temp = max_safe_temp

    # Simulating the temperature path over time. Including the amount of time steps, the initial temperature, and the noise standard deviation.
    def simulate_temperature_path(self, time_steps=252, initial_temp=40, noise_std=1.25):

        # Creating an array that represents the time steps for the simulation
        time = np.arange(time_steps)

        # Defining the target operating temperature and the cooling rate constant for the Newton's Law of Cooling model.
        target_operating_temp = 80
        k_cooling_rate = 0.05

        # Using Newton's Law of Cooling to calculate the deterministic temperature path over time
        deterministic_temp = target_operating_temp + (initial_temp - target_operating_temp) * np.exp(-k_cooling_rate * time)

        # Creating sensor noise using a normal distrubtion and then adding it to our deterministic temperature path to simulate the noisy sensor readings
        sensor_noise = np.random.normal(loc=0, scale=noise_std, size=time_steps)
        simulated_temp = deterministic_temp + sensor_noise

        # Creating a DataFrame to store the time steps, simulated temperature readings, and the max safe limit.
        df = pd.DataFrame({
            'Time_Step': time,
            'Temperature_C': simulated_temp,
            'Max_Safe_Limit_C': self.max_safe_temp
        })
        
        return df

# Testing the ThermalCoolingLoop class and the outputs
if __name__ == "__main__":
    model = ThermalCoolingLoop()
    df_sample = model.simulate_temperature_path()
    print("Thermal Simulation Sample Data:")
    print(df_sample.head())