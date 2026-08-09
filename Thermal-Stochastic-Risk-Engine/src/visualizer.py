import matplotlib.pyplot as plt
import numpy as np
import os

# Creating a visualizer class for the thermal model and the quant engine
class RiskEngineVisualizer:

    # Creating the visualizer styler and making a data folder if there isn't one
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

        if not os.path.exists('data'):
            os.makedirs('data')
            print("Successfully created missing 'data/' directory.")

    # Plotting the thermal sensor data 
    def plot_thermal_sensor_data(self, df_thermal):
        plt.figure(figsize=(10, 5))
        
        # Plot the noisy sensor temperature path
        plt.plot(df_thermal['Time_Step'], df_thermal['Temperature_C'], 
                 label='Simulated Sensor Temp (°C)', color='#1f77b4', linewidth=1.5)
        
        # Plot the critical threshold limit line
        plt.axhline(y=df_thermal['Max_Safe_Limit_C'].iloc[0], 
                    color='red', linestyle='--', linewidth=2, label='Max Safe Limit (90°C)')

        # Adjust margins, labels, title, and legend
        plt.margins(x=0.1,y=0.25)
        plt.title('Phase 1: Thermal Cooling Loop Sensor Data & Noise Simulation', fontsize=12, fontweight='bold')
        plt.xlabel('Time Steps', fontsize=10)
        plt.ylabel('Temperature (°C)', fontsize=10)
        plt.legend(loc='upper right')
        plt.tight_layout()
        
        # Save plot in data folder and show it
        plt.savefig('data/thermal_sensor_plot.png', dpi=300)
        plt.show()

    # Plotting the Monte Carlo quant engine
    def plot_monte_carlo_paths(self, paths, title="Monte Carlo Simulation Paths"):
        plt.figure(figsize=(10, 5))
        
        # Plotting all paths with low opacity to show density distribution
        plt.plot(paths, color='#1f77b4', alpha=0.05, linewidth=1)
        
        # Plotting the mean path
        mean_path = np.mean(paths, axis=1)
        plt.plot(mean_path, color='#ff7f0e', linewidth=2.5, label='Expected Path (Mean)')

        # Adjust margins, labels, title, and legend
        plt.title(title, fontsize=12, fontweight='bold')
        plt.xlabel('Time Steps', fontsize=10)
        plt.ylabel('Value / Price', fontsize=10)
        plt.legend(loc='upper left')
        plt.tight_layout()
        
        # Save plot in data folder and show it
        plt.savefig('data/monte_carlo_paths_plot.png', dpi=300)
        plt.show()

    # Calculating the value at risk and the conditional value at risk
    def calculate_var_cvar(self, stock_paths, initial_price=100, confidence_level=0.95):

        # Making variables for the formula
        initial_price = stock_paths [0]
        final_prices = stock_paths[-1]

        # forcing intital price to be a float if it is a list or array
        if hasattr(initial_price, '__len__') and not isinstance(initial_price, (str, bytes)):
            portfolio_value = float(np.mean(initial_price))
        else:
            portfolio_value = float(initial_price)

        # Creating the return variable "L"
        returns = (final_prices - initial_price) / initial_price

        # Making the return threshold as percentile
        alpha_percentile = 1-confidence_level
        return_threshold = np.percentile(returns, alpha_percentile * 100).item()

        #Making the VaR
        var = float(-portfolio_value * return_threshold)

        # Making the CVaR
        worst_returns = returns[returns <= return_threshold]
        cvar = float(-portfolio_value * np.mean(worst_returns))

        return var, cvar


# Testing the RiskEngineVisualizer class and the outputs
if __name__ == "__main__":

    # Test Visualizer with our da
    from thermal_model import ThermalCoolingLoop
    from quant_engine import StochasticRiskEngine
    
    vis = RiskEngineVisualizer()
    
    # Test Thermal Plot
    thermal_model = ThermalCoolingLoop()
    df_test = thermal_model.simulate_temperature_path()
    vis.plot_thermal_sensor_data(df_test)
    
    # Test Quant GBM Plot
    quant_engine = StochasticRiskEngine(num_simulations=1000, time_steps=252)
    gbm_test = quant_engine.simulate_gbm_stock_paths()
    vis.plot_monte_carlo_paths(gbm_test, title="Phase 2: GBM Stock Price Paths")