import time
from pathlib import Path
from src.experiment.batch import BatchDownloader
from src.experiment.catalog import DataCatalog

if __name__ == "__main__":
    print("=====================================================")
    print("   PATTERN DISCOVERY LAB: PLATFORM VALIDATION TEST   ")
    print("=====================================================")

    workspace_name = "alpha_core_test"
    tickers = ["RELIANCE.NS", "HDFCBANK.NS"]
    
    # Initialize the Batch Engine (which wraps the ExperimentManager)
    batch = BatchDownloader(max_workers=2)

    # ---------------------------------------------------------
    # TEST 1: Workspaces, Lifecycle States, Manifests, & YAMLs
    # ---------------------------------------------------------
    print(f"\n[1] Testing Network Download & Artifact Generation...")
    start_t = time.time()
    
    # This will trigger state transitions (CREATED -> RUNNING -> COMPLETED)
    # and build the nested workspace hierarchy.
    batch.execute_batch(
        tickers=tickers, 
        start="2023-01-01", 
        end="2023-01-05", 
        workspace=workspace_name
    )
    
    print(f"> Network Fetch completed in {time.time() - start_t:.2f} seconds.")

    # ---------------------------------------------------------
    # TEST 2: The Idempotent Cache
    # ---------------------------------------------------------
    print(f"\n[2] Testing Idempotent Caching Layer (Should be < 0.2s)...")
    start_t = time.time()
    
    # Requesting the exact same data. The system should intercept this 
    # using DuckDB and serve from the Parquet files.
    batch.execute_batch(
        tickers=tickers, 
        start="2023-01-01", 
        end="2023-01-05", 
        workspace=workspace_name
    )
    
    print(f"> Cache Hit completed in {time.time() - start_t:.2f} seconds.")

    # ---------------------------------------------------------
    # TEST 3: DuckDB Data Catalog
    # ---------------------------------------------------------
    print(f"\n[3] Testing DuckDB Relational Indexing...")
    catalog = DataCatalog()
    
    df = catalog.query(f"""
        SELECT experiment_id, ticker, status, execution_ms 
        FROM experiments 
        WHERE workspace = '{workspace_name}'
    """)
    print("\n--- DuckDB Table Output ---")
    print(df)

    # ---------------------------------------------------------
    # TEST 4: Physical File System Audit
    # ---------------------------------------------------------
    print(f"\n[4] Physical File System Audit...")
    
    if not df.empty:
        exp_id = df.iloc[0]['experiment_id']
        test_path = Path(f"workspaces/{workspace_name}/{exp_id}")
        
        print(f"Inspecting {test_path}...")
        print(f" - experiment.yaml exists : {(test_path / 'experiment.yaml').exists()}")
        print(f" - manifest.json exists   : {(test_path / 'manifest.json').exists()}")
        print(f" - market_data.parquet    : {(test_path / 'market_data.parquet').exists()}")
    else:
        print("ERROR: Catalog returned empty dataframe. Something is wrong.")
        
    print("\n=====================================================")
    print("              VALIDATION COMPLETE                    ")
    print("=====================================================")