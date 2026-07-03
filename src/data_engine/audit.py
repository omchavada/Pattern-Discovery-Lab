"""
Audit and telemetry recording for the data pipeline.
"""

import hashlib
import platform
import time
from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class AuditRecord:
    """
    Immutable ledger tracking the lineage, performance, and environment of a pipeline run.
    """

    # System & Environment Lineage
    python_version: str = platform.python_version()
    system_os: str = platform.system()

    # Data Lineage
    file_hash: str = ""
    rows_processed: int = 0

    # Telemetry (Profiling)
    step_times_ms: dict[str, float] = field(default_factory=dict)

    @property
    def total_execution_ms(self) -> float:
        """Calculates total pipeline execution time from tracked steps."""
        return round(sum(self.step_times_ms.values()), 2)

    def record_lineage(self, df: pd.DataFrame) -> None:
        """
        Calculates a SHA-256 hash of the DataFrame to ensure cryptographic
        immutability tracking for future audits.
        """
        if not df.empty:
            self.rows_processed = len(df)
            # Hash the underlying pandas values for a unique state signature
            hashed = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
            self.file_hash = hashed


class StepProfiler:
    """
    Context manager to precisely time individual pipeline stages.
    """

    def __init__(self, audit_record: AuditRecord, step_name: str) -> None:
        self.audit = audit_record
        self.step_name = step_name
        self.start_time = 0.0

    def __enter__(self) -> "StepProfiler":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        self.audit.step_times_ms[self.step_name] = round(elapsed_ms, 2)
