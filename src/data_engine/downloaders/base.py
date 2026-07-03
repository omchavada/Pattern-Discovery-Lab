"""
Abstract Base Class for specific data source downloaders.
"""

import abc

from src.common.interfaces import BaseDataFeed
from src.data_engine.types import DateStr, MarketData, Ticker


class BaseDownloader(BaseDataFeed):
    """
    Base contract for all external data fetchers within the Data Engine.
    Inherits from the platform-wide BaseDataFeed interface.
    """

    @abc.abstractmethod
    def fetch_historical(self, ticker: Ticker, start: DateStr, end: DateStr) -> MarketData:
        """
        Fetch historical OHLCV data for a specific ticker.
        """
        pass
