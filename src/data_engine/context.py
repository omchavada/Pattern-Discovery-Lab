"""
Pipeline Context for tracking data state through the ETL process.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import pandas as pd
import time

from src.data_engine.types import Ticker
from src.data_engine.validators.report import ValidationReport

@dataclass
class PipelineContext:
    """
    Carries the state of market data through the Download -> Standardize -> Validate -> Clean pipeline.
    """
    ticker: Ticker
    source: str
    
    # Timing and Metadata
    start_time: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Data States (Immutable at each stage)
    raw_data: Optional[pd.DataFrame] = None
    market_data: Optional[pd.DataFrame] = None
    cleaned_data: Optional[pd.DataFrame] = None
    
    # Reports
    validation_report: Optional[ValidationReport] = None

    @property
    def execution_time_ms(self) -> float:
        """Returns the pipeline execution time in milliseconds."""
        return round((time.time() - self.start_time) * 1000, 2)