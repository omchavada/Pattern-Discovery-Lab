"""
The unified state container for a complete research experiment.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import pandas as pd

from src.data_engine.validators.report import ValidationReport
from src.data_engine.audit import AuditRecord

@dataclass
class ExperimentContext:
    """
    The master ledger tracking an entire alpha research lifecycle.
    """
    experiment_id: str
    name: str
    ticker: str
    source: str
    
    # Telemetry & Lineage
    audit: AuditRecord = field(default_factory=AuditRecord)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 1. Data Phase
    raw_data: Optional[pd.DataFrame] = None
    market_data: Optional[pd.DataFrame] = None
    validation_report: Optional[ValidationReport] = None
    
    # 2. Feature Phase (Placeholders for future sprints)
    # features_data: Optional[pd.DataFrame] = None
    
    # 3. Hypothesis Phase
    # signals_data: Optional[pd.DataFrame] = None
    
    # 4. Backtest Phase
    # backtest_metrics: Dict[str, float] = field(default_factory=dict)