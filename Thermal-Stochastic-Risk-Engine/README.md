# Thermal & Stochastic Risk Engine

A hybrid quantitative risk modeling framework that bridges physical hardware engineering simulations (thermal cooling loops with sensor noise) with institutional quantitative finance techniques (Monte Carlo simulations and Geometric Brownian Motion paths).

# Project Architecture

The project is structured into different components, separating thermal sensor modeling, stochastic mathematics, and visualization:

Thermal-Stochastic-Risk-Engine/
│
├── data/                        # Output directory for plots
│   ├── thermal_sensor_plot.png
│   └── monte_carlo_paths_plot.png
│
├── src/                         # Core logic modules
│   ├── __init__.py
│   ├── thermal_model.py         # Phase 1: Physical cooling loop & noise
│   ├── quant_engine.py          # Phase 2: Monte Carlo & GBM engine
│   └── visualizer.py            # Phase 3: Matplotlib charts
│
├── main.py                      # Orchestrator script
└── README.pdf                   # Project documentation

# Thought process

My thought process can be found in a pdf document titled README.

# Quick Start & Installation
Clone the repository:
git clone [https://github.com/your-username/Thermal-Stochastic-Risk-Engine.git](https://github.com/your-username/Thermal-Stochastic-Risk-Engine.git)
cd Thermal-Stochastic-Risk-Engine

Install dependencies:
Ensure you have Python installed, then install the required numerical and plotting libraries:
pip install numpy pandas matplotlib

Run the full execution pipeline:
python main.py

This will run all simulations, calculate risk metrics, and automatically generate figures in the data/ folder.
