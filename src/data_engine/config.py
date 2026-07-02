"""
Configuration settings for the Data Engine.
"""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# The Immutable Data Hierarchy
RAW_DATA_PATH = DATA_DIR / "raw"
VALIDATED_DATA_PATH = DATA_DIR / "validated"
CLEAN_DATA_PATH = DATA_DIR / "clean"
DB_PATH = DATA_DIR / "database" / "market_data.db"

# Engine Constants
DEFAULT_TIMEOUT = 10  # seconds
MAX_RETRIES = 3