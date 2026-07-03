"""
Unit tests for the Data Validation Engine.
"""
import pytest
import pandas as pd
from src.data_engine.validators.price import PriceValidator
from src.data_engine.validators.report import ValidationReport

def test_price_validator_catches_negative_prices():
    """Ensures the PriceValidator flags negative values and drops the quality score."""
    
    # 1. Arrange: Create mock standardized data with a negative low price
    mock_data = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "open": [100.0, 105.0],
        "high": [110.0, 108.0],
        "low": [95.0, -5.0],  # <-- Bad data injected here
        "close": [105.0, 102.0],
        "volume": [1000, 1200],
        "ticker": ["RELIANCE.NS", "RELIANCE.NS"]
    })
    
    validator = PriceValidator()
    report = ValidationReport(ticker="RELIANCE.NS", total_rows=2)
    
    # 2. Act: Run the validation (it returns the df, and updates report in-place)
    result_df = validator.validate(mock_data, report)
    
    # 3. Assert: Verify the bouncer did its job by checking the original report
    assert not report.passed, "Validator failed to flag the dataset as failed."
    assert report.quality_score < 100.0, "Quality score was not penalized."
    
    # Verify the exact issue was logged
  # Verify the exact issue was logged
    # Change .description to .message
    issue_found = any("Negative prices detected" in issue.message for issue in report.issues)
    assert issue_found, "The specific negative price issue was not logged."