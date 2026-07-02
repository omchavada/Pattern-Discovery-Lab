"""
Pipeline Context for tracking data state through the ETL process.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import pandas as pd

from src.data_engine.types import Ticker
from src.data_engine.validators.report import ValidationReport
from src.data_engine.audit import AuditRecord

@dataclass
class PipelineContext:
    """
    Carries the state, audit trail, and validation reports through the ETL pipeline.
    """
    ticker: Ticker
    source: str
    
    # Flight Data Recorder
    audit: AuditRecord = field(default_factory=AuditRecord)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Immutable Data States
    raw_data: Optional[pd.DataFrame] = None
    market_data: Optional[pd.DataFrame] = None
    cleaned_data: Optional[pd.DataFrame] = None
    
    # Reports
    validation_report: Optional[ValidationReport] = None