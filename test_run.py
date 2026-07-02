# test_run.py
from src.data_engine import DataEngine

if __name__ == "__main__":
    ticker = "RELIANCE.NS"
    
    # Instantiate the unified engine
    engine = DataEngine()
    
    # 1. The one-line download command
    print("\n--- Testing Engine Download ---")
    engine.download(ticker, start="2023-01-01", end="2023-01-15")
    
    # 2. The one-line load command
    print("\n--- Testing Engine Load ---")
    df = engine.load(ticker)
    
    print("\nFinal Output:")
    print(df.head())