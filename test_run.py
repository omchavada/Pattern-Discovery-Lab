# test_run.py
from src.data_engine.downloaders.yahoo import YahooDownloader

if __name__ == "__main__":
    downloader = YahooDownloader()
    downloader.connect()
    
    # Let's test the fetch
    df = downloader.fetch_historical("RELIANCE.NS", "2023-01-01", "2023-01-10")
    print(df.head())