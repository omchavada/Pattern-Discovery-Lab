"""
Core architectural interfaces for the trading platform.
"""

import abc

import pandas as pd


class BaseDataFeed(abc.ABC):
    """Abstract Base Class for all data feeds."""

    @abc.abstractmethod
    def connect(self) -> bool:
        pass

    @abc.abstractmethod
    def get_historical_data(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        pass


# (You can leave the BaseBroker, BaseFeature, BaseStrategy classes out for now to keep it simple,
#  or paste the full block from our earlier chat).
