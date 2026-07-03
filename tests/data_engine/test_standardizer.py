"""
Unit tests for the YahooStandardizer.
"""
import pandas as pd
from src.data_engine.standardizers.yahoo import YahooStandardizer

def test_yahoo_standardizer_column_formatting():
    """Tests if raw Yahoo Finance columns are correctly standardized."""
    
    # 1. Arrange: Create mock raw data exactly as yfinance returns it
    # 1. Arrange: Create mock raw data exactly as yfinance returns it
    mock_index = pd.Index(pd.to_datetime(["2023-01-01"]), name="Date")
    
    mock_raw_data = pd.DataFrame({
        "Open": [100.0],
        "High": [105.0],
        "Low": [95.0],
        "Close": [102.0],
        "Volume": [1000]
    }, index=mock_index)
    
    standardizer = YahooStandardizer()
    ticker = "RELIANCE.NS"
    
    # 2. Act: Run the standardization process
    result_df = standardizer.standardize(mock_raw_data, ticker)
    
    # 3. Assert: Verify the outputs
    assert not result_df.empty, "Standardizer returned an empty DataFrame"
    
    # Check that columns were lowercased and the index was reset to 'date'
    expected_columns = ["date", "open", "high", "low", "close", "volume", "ticker"]
    for col in expected_columns:
        assert col in result_df.columns, f"Missing expected column: {col}"
        
    # Check that the ticker was injected correctly
    assert result_df.iloc[0]["ticker"] == "RELIANCE.NS"