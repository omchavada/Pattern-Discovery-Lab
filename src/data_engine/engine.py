"""
The public facade for the Data Engine module.
"""
import logging
from typing import Optional

from src.data_engine.types import Ticker, DateStr, MarketData
from src.data_engine.config import RAW_DATA_PATH
from src.data_engine.downloaders.yahoo import YahooDownloader
from src.data_engine.storage.parquet import ParquetStorage

# Setup module-level logger
logger = logging.getLogger(__name__)

class DataEngine:
    """
    Orchestrates the downloading, validation, storage, and retrieval 
    of market data and metadata.
    """
    
    def __init__(self):
        # Initialize internal worker modules
        self.downloader = YahooDownloader()
        self.storage = ParquetStorage(RAW_DATA_PATH)
        # self.validator = MarketValidator()  # We will wire this in Milestone 2.5
        
        logger.info("DataEngine Facade initialized.")
        
    def download(self, ticker: Ticker, start: DateStr, end: DateStr) -> bool:
        """
        Downloads data via the active downloader and saves it to storage.
        """
        logger.info(f"DataEngine: Starting download process for {ticker}")
        try:
            # 1. Fetch
            df = self.downloader.fetch_historical(ticker, start, end)
            
            # 2. Validate (Placeholder for next sprint)
            # self.validator.validate(df)
            
            # 3. Save
            success = self.storage.save(df, ticker)
            
            logger.info(f"DataEngine: Successfully downloaded and stored {ticker}")
            return success
            
        except Exception as e:
            logger.error(f"DataEngine: Failed to process {ticker} - {str(e)}")
            return False

    def load(self, ticker: Ticker) -> MarketData:
        """
        Loads processed data from storage into memory.
        """
        logger.info(f"DataEngine: Loading data for {ticker}")
        return self.storage.load(ticker)