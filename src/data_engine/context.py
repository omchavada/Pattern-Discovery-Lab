"""
Pipeline Context for tracking data state through the ETL process.
"""

from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from src.data_engine.audit import AuditRecord
from src.data_engine.types import Ticker
from src.data_engine.validators.report import ValidationReport


@dataclass
class PipelineContext:
    """
    Carries the state, audit trail, and validation reports through the ETL pipeline.
    """

    ticker: Ticker
    source: str

    # Flight Data Recorder
    audit: AuditRecord = field(default_factory=AuditRecord)
    metadata: dict[str, Any] = field(default_factory=dict)

    # Immutable Data States
    raw_data: pd.DataFrame | None = None
    market_data: pd.DataFrame | None = None
    cleaned_data: pd.DataFrame | None = None

    # Reports
    validation_report: ValidationReport | None = None
