"""
Configuration settings for the Data Engine.
"""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(os.path.abspath(__file__)).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"
DB_PATH = DATA_DIR / "database" / "market_data.db"

# Engine Constants
DEFAULT_TIMEOUT = 10  # seconds
MAX_RETRIES = 3