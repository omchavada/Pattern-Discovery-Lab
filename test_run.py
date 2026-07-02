import time
from src.experiment.batch import BatchDownloader
from src.experiment.catalog import DataCatalog

if __name__ == "__main__":
    print("--- Booting High-Throughput Research OS ---")
    
    # Define a basket of tickers to fetch concurrently
    ticker_basket = ["TCS.NS", "INFY.NS", "WIT.NS", "RELIANCE.NS", "HDFCBANK.NS"]
    
    start_time = time.time()
    
    # Initialize the batch downloader with 5 parallel worker threads
    batch_engine = BatchDownloader(max_workers=5)
    
    print(f"\n--- 1. Launching Concurrent Downloads for {len(ticker_basket)} Stocks ---")
    contexts = batch_engine.execute_batch(
        tickers=ticker_basket,
        start="2023-01-01",
        end="2023-01-15",
        workspace="large_cap_momentum"
    )
    
    elapsed_time = time.time() - start_time
    print(f"\nBatch processing completed in {elapsed_time:.2f} seconds.")
    
    print("\n--- 2. Querying Data Catalog for the New Workspace ---")
    catalog = DataCatalog()
    df_workspace = catalog.query("""
        SELECT experiment_id, ticker, quality_score, execution_ms, status 
        FROM experiments 
        WHERE workspace = 'large_cap_momentum'
    """)
    print(df_workspace)