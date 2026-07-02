"""
Parquet implementation for local file-based storage.
"""
import logging
from pathlib import Path
import pandas as pd

from src.data_engine.types import Ticker, MarketData
from src.data_engine.storage.base import BaseStorage
from src.data_engine.exceptions import StorageError

# Setup module-level logger
logger = logging.getLogger(__name__)

class ParquetStorage(BaseStorage):
    """
    Handles reading and writing compressed .parquet files to the local disk.
    """
    
    def __init__(self, storage_path: Path | str):
        """
        Initializes the storage manager and ensures the target directory exists.
        """
        self.storage_path = Path(storage_path)
        # Create the directory if it doesn't exist yet
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"ParquetStorage initialized at {self.storage_path}")

    def _get_file_path(self, ticker: Ticker) -> Path:
        """Helper method to construct the exact file path."""
        return self.storage_path / f"{ticker}.parquet"

    def save(self, data: MarketData, ticker: Ticker) -> bool:
        """
        Writes the DataFrame to {storage_path}/{ticker}.parquet.
        """
        try:
            file_path = self._get_file_path(ticker)
            # PyArrow engine is standard for quant systems
            data.to_parquet(file_path, engine='pyarrow', index=False)
            logger.info(f"Successfully saved {len(data)} rows for {ticker} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save data for {ticker}: {str(e)}")
            raise StorageError(f"Could not save {ticker}.parquet") from e

    def load(self, ticker: Ticker) -> MarketData:
        """
        Reads the DataFrame from {storage_path}/{ticker}.parquet.
        """
        file_path = self._get_file_path(ticker)
        
        if not file_path.exists():
            raise StorageError(f"No data found for {ticker} at {file_path}")
            
        try:
            df = pd.read_parquet(file_path, engine='pyarrow')
            logger.info(f"Successfully loaded {len(df)} rows for {ticker} from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Failed to load data for {ticker}: {str(e)}")
            raise StorageError(f"Could not read {ticker}.parquet") from e