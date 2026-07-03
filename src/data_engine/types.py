"""
Core type definitions for the Data Engine.
"""

from typing import Any

import pandas as pd

# Modern Python type aliases (PEP 695)
type Ticker = str
type DateStr = str
type MarketData = pd.DataFrame
type JSONDict = dict[str, Any]
