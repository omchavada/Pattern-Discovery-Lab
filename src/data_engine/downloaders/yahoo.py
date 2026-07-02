"""
Yahoo Finance implementation of the BaseDownloader.
"""
import time
import logging
import pandas as pd
import yfinance as yf

from src.data_engine.types import Ticker, DateStr, MarketData
from src.data_engine.downloaders.base import BaseDownloader
from src.data_engine.exceptions import DataDownloadError
from src.data_engine.config import MAX_RETRIES, DEFAULT_TIMEOUT

# Setup module-level logger
logger = logging.getLogger(__name__)

class YahooDownloader(BaseDownloader):
    """
    Downloads end-of-day market data from Yahoo Finance via yfinance.
    """
    
    def connect(self) -> bool:
        """
        yfinance operates via REST and doesn't require a persistent WebSocket connection.
        We return True to satisfy the BaseDataFeed interface.
        """
        logger.info("YahooDownloader initialized (REST mode).")
        return True
        
    def get_historical_data(self, ticker: Ticker, start: DateStr, end: DateStr) -> MarketData:
        """
        Implements the platform-wide BaseDataFeed contract.
        Routes directly to fetch_historical.
        """
        return self.fetch_historical(ticker, start, end)

    def fetch_historical(self, ticker: Ticker, start: DateStr, end: DateStr) -> MarketData:
        """
        Executes the API call to Yahoo Finance, applying retry logic 
        and timeout configurations.
        """
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Fetching {ticker} from {start} to {end} (Attempt {attempt}/{MAX_RETRIES})")
                
                # Fetch data via yfinance
                df = yf.download(
                    tickers=ticker,
                    start=start,
                    end=end,
                    timeout=DEFAULT_TIMEOUT,
                    progress=False
                )
                
                if df.empty:
                    raise DataDownloadError(f"Yahoo Finance returned empty DataFrame for {ticker}.")
                
                # Clean up yfinance's multi-level column formatting if it appears
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                # Standardize the DataFrame index and columns
                df = df.reset_index()
                df.columns = [str(col).lower().replace(" ", "_") for col in df.columns]
                
                # Ensure our primary key exists
                df['ticker'] = ticker
                
                logger.info(f"Successfully downloaded {len(df)} rows for {ticker}.")
                return df
                
            except Exception as e:
                logger.warning(f"Download failed for {ticker}: {str(e)}")
                if attempt == MAX_RETRIES:
                    logger.error(f"Max retries reached. Could not fetch {ticker}.")
                    raise DataDownloadError(f"Failed to fetch {ticker} after {MAX_RETRIES} attempts.") from e
                
                # Exponential backoff before retry (2s, 4s, 8s...)
                time.sleep(2 ** attempt)