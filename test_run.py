from src.experiment.manager import ExperimentManager
from src.experiment.catalog import DataCatalog

if __name__ == "__main__":
    manager = ExperimentManager()
    
    print("--- 1. Generating Mock Experiments ---")
    # Run a Momentum experiment
    manager.run_experiment(name="Reliance Base", ticker="RELIANCE.NS", start="2023-01-01", end="2023-01-15", workspace="momentum")
    # Run a Mean Reversion experiment
    manager.run_experiment(name="HDFC Base", ticker="HDFCBANK.NS", start="2023-01-01", end="2023-01-15", workspace="mean_reversion")

    print("\n--- 2. Querying the Data Catalog ---")
    catalog = DataCatalog()
    
    print("\nAll Experiments in the OS:")
    df_all = catalog.get_all_experiments()
    print(df_all[['workspace', 'experiment_id', 'ticker', 'quality_score', 'status']])
    
    print("\nCustom SQL Query (Show me Momentum datasets only):")
    df_sql = catalog.query("SELECT experiment_id, ticker, dataset_sha256 FROM experiments WHERE workspace = 'momentum'")
    print(df_sql)