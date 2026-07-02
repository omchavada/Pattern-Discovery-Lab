"""
Local file-system implementation of the Experiment Tracker.
"""
import json
import logging
from pathlib import Path
from typing import Any
import pandas as pd

from src.experiment.interfaces import BaseTracker
from src.data_engine.config import PROJECT_ROOT
from src.experiment.context import ExperimentContext

logger = logging.getLogger(__name__)

class FileTracker(BaseTracker):
    """
    Saves artifacts (Parquet), metrics (JSON), and audits (JSON) to the local disk.
    """
    
    def __init__(self, base_dir: Path = PROJECT_ROOT / "experiments"):
        self.base_dir = Path(base_dir)

    def _get_exp_dir(self, experiment_id: str) -> Path:
        return self.base_dir / experiment_id

    def log_artifact(self, experiment_id: str, name: str, data: Any) -> None:
        """
        Saves a DataFrame as a Parquet file inside the experiment folder.
        """
        exp_dir = self._get_exp_dir(experiment_id)
        
        if isinstance(data, pd.DataFrame):
            file_path = exp_dir / f"{name}.parquet"
            data.to_parquet(file_path, engine='pyarrow', index=False)
            logger.info(f"Logged artifact {name}.parquet to {experiment_id}")
        else:
            logger.warning(f"Unsupported artifact type for {name}. Only DataFrames are supported currently.")

    def log_metric(self, experiment_id: str, key: str, value: float) -> None:
        """
        Appends a key-value metric to the experiment's metrics.json file.
        """
        exp_dir = self._get_exp_dir(experiment_id)
        metrics_file = exp_dir / "metrics.json"
        
        metrics = {}
        if metrics_file.exists():
            with open(metrics_file, "r") as f:
                metrics = json.load(f)
                
        metrics[key] = value
        
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=4)
            
        logger.info(f"Logged metric {key}={value} to {experiment_id}")

    def log_context(self, ctx: ExperimentContext) -> None:
        """
        A macro-function that automatically saves all states of the ExperimentContext.
        """
        logger.info(f"Finalizing tracking for {ctx.experiment_id}...")
        
        # 1. Log Data Artifacts
        if ctx.raw_data is not None:
            self.log_artifact(ctx.experiment_id, "raw_data", ctx.raw_data)
        if ctx.market_data is not None:
            self.log_artifact(ctx.experiment_id, "market_data", ctx.market_data)
            
        # 2. Log Audit & Telemetry
        exp_dir = self._get_exp_dir(ctx.experiment_id)
        audit_file = exp_dir / "audit.json"
        
        # Convert dataclasses/enums to serializable dicts
        audit_dict = {
            "name": ctx.name,
            "ticker": ctx.ticker,
            "source": ctx.source,
            "audit": {
                "python_version": ctx.audit.python_version,
                "system_os": ctx.audit.system_os,
                "dataset_sha256": ctx.audit.file_hash,
                "rows_processed": ctx.audit.rows_processed,
                "total_execution_ms": ctx.audit.total_execution_ms,
                "step_times_ms": ctx.audit.step_times_ms
            }
        }
        
        with open(audit_file, "w") as f:
            json.dump(audit_dict, f, indent=4)