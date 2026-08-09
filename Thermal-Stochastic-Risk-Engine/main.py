from src.thermal_model import ThermalCoolingLoop
from src.quant_engine import StochasticRiskEngine
from src.visualizer import RiskEngineVisualizer

# Main function to run the entire pipeline
def main():
    print("==================================================")
    print(" Starting Thermal-Stochastic-Risk-Engine Pipeline")
    print("==================================================")

    # Running the Thermal System Sensor Simulation
    print("\n[Phase 1] Simulating physical thermal cooling loop...")
    thermal_model = ThermalCoolingLoop(ambient_temp=20, max_safe_temp=90)
    df_thermal = thermal_model.simulate_temperature_path(time_steps=252)
    print(f"-> Generated {len(df_thermal)} steps of thermal sensor data.")

    # Running theStochastic Risk Engine (GBM & Risk Analysis quant engine)
    print("\n[Phase 2] Running Monte Carlo simulations & Risk Engine...")
    quant_engine = StochasticRiskEngine(num_simulations=1000, time_steps=252)
    
    # Simulate financial stock paths (GBM)
    stock_paths = quant_engine.simulate_gbm_stock_paths(s0=100.0, mu=0.07, sigma=0.13)
    print(f"-> Simulated GBM stock paths shape: {stock_paths.shape}")
    print(f"-> Expected Final Stock Price: ${np.mean(stock_paths[-1]):.2f}")

    # Generate multi-path thermal scenarios to calculate physical failure risk
    mock_thermal_matrix = np.random.normal(loc=80, scale=2.5, size=(252, 1000))
    fail_prob = quant_engine.calculate_thermal_failure_probability(mock_thermal_matrix, max_safe_limit=90)
    print(f"-> Calculated Thermal Overheat Failure Probability: {fail_prob * 100:.2f}%")

    # Running the visualizations & saving the outputs
    print("\n[Phase 3 & 4] Generating and saving charts...")
    visualizer = RiskEngineVisualizer()
    
    # Save thermal plot
    visualizer.plot_thermal_sensor_data(df_thermal)
    
    # Save Monte Carlo stock path plot
    visualizer.plot_monte_carlo_paths(stock_paths, title="Phase 2: GBM Stock Price Paths (Monte Carlo)")
    
    # Calculate and display VaR and CVaR
    var, cvar = visualizer.calculate_var_cvar(stock_paths, initial_price=100.0, confidence_level=0.95)
    print(f"-> Value at Risk (VaR): ${var:.2f}")
    print(f"-> Conditional Value at Risk (CVaR): ${cvar:.2f}")

    print("\n==================================================")
    print(" Pipeline Execution Complete! Check the 'data/' folder.")
    print("==================================================")

if __name__ == "__main__":
    import numpy as np
    main()