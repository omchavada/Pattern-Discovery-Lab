# test_run.py
from src.data_engine.downloaders.yahoo import YahooDownloader
from src.data_engine.storage.parquet import ParquetStorage
from src.data_engine.config import RAW_DATA_PATH

if __name__ == "__main__":
    ticker = "RELIANCE.NS"
    
    # 1. Download the data
    print("--- 1. Fetching Data ---")
    downloader = YahooDownloader()
    df = downloader.fetch_historical(ticker, "2023-01-01", "2023-01-10")
    print(f"Downloaded {len(df)} rows.")
    
    # 2. Save to Parquet
    print("\n--- 2. Saving to Parquet ---")
    storage = ParquetStorage(RAW_DATA_PATH)
    storage.save(df, ticker)
    
    # 3. Load from Parquet to verify
    print("\n--- 3. Loading from Disk ---")
    loaded_df = storage.load(ticker)
    print(loaded_df.head())