"""
Yahoo Finance specific data standardizer.
"""

import logging

import pandas as pd

from src.data_engine.standardizers.base import BaseStandardizer
from src.data_engine.types import MarketData, Ticker

logger = logging.getLogger(__name__)


class YahooStandardizer(BaseStandardizer):
    """
    Transforms yfinance payloads into canonical MarketData.
    """

    def standardize(self, df: pd.DataFrame, ticker: Ticker) -> MarketData:
        logger.info(f"Standardizing Yahoo Finance payload for {ticker}...")

        # 1. Protect original data
        standard_df = df.copy()

        # 2. Flatten MultiIndex if yfinance returned one
        if isinstance(standard_df.columns, pd.MultiIndex):
            standard_df.columns = standard_df.columns.droplevel(1)

        # 3. Canonical Column Names
        standard_df.columns = [
            str(col).lower().strip().replace(" ", "_") for col in standard_df.columns
        ]

        # 4. Extract and Canonicalize Date Index
        if (
            "date" not in standard_df.columns
            and standard_df.index.name
            and standard_df.index.name.lower() == "date"
        ):
            standard_df = standard_df.reset_index()
            standard_df.rename(columns={standard_df.columns[0]: "date"}, inplace=True)

        # 5. Timezone Normalization (Naive UTC)
        if "date" in standard_df.columns:
            standard_df["date"] = pd.to_datetime(standard_df["date"], utc=True).dt.tz_localize(None)

        # 6. Type Casting
        for col in ["open", "high", "low", "close", "adj_close"]:
            if col in standard_df.columns:
                standard_df[col] = standard_df[col].astype(float)

        if "volume" in standard_df.columns:
            standard_df["volume"] = standard_df["volume"].astype("int64")

        # 7. Append Primary Key and Sort
        standard_df["ticker"] = ticker
        standard_df = standard_df.sort_values(by="date", ascending=True).reset_index(drop=True)

        return standard_df
