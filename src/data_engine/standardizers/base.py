"""
Abstract Base Class for broker-specific standardizers.
"""
import abc
import pandas as pd
from src.data_engine.types import Ticker, MarketData

class BaseStandardizer(abc.ABC):
    """
    Contract for mapping broker-specific data schemas into the 
    platform's canonical MarketData format.
    """
    
    @abc.abstractmethod
    def standardize(self, df: pd.DataFrame, ticker: Ticker) -> MarketData:
        """
        Applies non-destructive transformations (typing, sorting, column renaming).
        """
        pass