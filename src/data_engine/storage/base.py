"""
Abstract Base Class for data storage mechanisms.
"""
import abc
from src.data_engine.types import Ticker, MarketData

class BaseStorage(abc.ABC):
    """
    Standardizes how the engine saves and loads processed market data.
    """
    
    @abc.abstractmethod
    def save(self, data: MarketData, ticker: Ticker) -> bool:
        """
        Persist the DataFrame to the storage medium.
        """
        pass

    @abc.abstractmethod
    def load(self, ticker: Ticker) -> MarketData:
        """
        Retrieve a DataFrame from the storage medium.
        """
        pass