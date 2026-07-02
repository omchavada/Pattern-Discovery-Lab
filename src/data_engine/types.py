"""
Type definitions and shared data structures for the Data Engine.
"""
from typing import TypeAlias, Dict, Any
import pandas as pd

# Type Aliases for clean hinting
Ticker: TypeAlias = str
DateStr: TypeAlias = str
MarketData: TypeAlias = pd.DataFrame
JSONDict: TypeAlias = Dict[str, Any]