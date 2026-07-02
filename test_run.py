# test_run.py
from src.experiment.manager import ExperimentManager

if __name__ == "__main__":
    print("--- Booting Pattern Discovery Lab ---")
    
    # Initialize the master manager
    manager = ExperimentManager()
    
    # Launch an experiment
    context = manager.run_experiment(
        name="Baseline Data Integrity Run",
        ticker="RELIANCE.NS",
        start="2023-01-01",
        end="2023-01-15",
        tags={"strategy": "momentum", "env": "dev"}
    )
    
    print("\n=========================================")
    print(f" EXPERIMENT {context.experiment_id} COMPLETE ")
    print("=========================================")
    print(f"Check the 'experiments/{context.experiment_id}' folder in your project root.")
    print("You will find your raw data, market data, and full audit JSON perfectly isolated.")