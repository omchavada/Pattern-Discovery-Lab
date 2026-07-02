"""
Local file-system implementation of the Experiment Tracker.
"""
import json
import logging
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd

from src.experiment.interfaces import BaseTracker
from src.data_engine.config import PROJECT_ROOT
from src.experiment.context import ExperimentContext
from src.experiment.state import ExperimentState

logger = logging.getLogger(__name__)

class FileTracker(BaseTracker):
    """
    Saves artifacts (Parquet), metrics, manifests, and configs to the local workspace.
    """
    
    def __init__(self, base_dir: Path = PROJECT_ROOT / "workspaces"):
        self.base_dir = Path(base_dir)

    def _get_exp_dir(self, workspace: str, experiment_id: str) -> Path:
        return self.base_dir / workspace / experiment_id

    def log_artifact(self, exp_dir: Path, name: str, data: Any) -> None:
        """Saves a DataFrame as a Parquet file."""
        if isinstance(data, pd.DataFrame):
            file_path = exp_dir / f"{name}.parquet"
            data.to_parquet(file_path, engine='pyarrow', index=False)
            logger.info(f"Logged artifact {name}.parquet")
            
    def log_metric(self, experiment_id: str, key: str, value: float) -> None:
        pass # Placeholder for Phase 3 (Backtesting)

    def log_context(self, ctx: ExperimentContext) -> None:
        """
        Finalizes the experiment by saving data, generating the YAML config, 
        and writing the searchable manifest.json.
        """
        exp_dir = self._get_exp_dir(ctx.workspace, ctx.experiment_id)
        
        # 1. Log Data Artifacts
        if ctx.raw_data is not None:
            self.log_artifact(exp_dir, "raw_data", ctx.raw_data)
        if ctx.market_data is not None:
            self.log_artifact(exp_dir, "market_data", ctx.market_data)
            
        # 2. Generate experiment.yaml (Reproducibility Config)
        config = {
            "experiment_id": ctx.experiment_id,
            "name": ctx.name,
            "ticker": ctx.ticker,
            "source": ctx.source,
            "workspace": ctx.workspace,
            "platform_version": "0.1.0-alpha"
        }
        with open(exp_dir / "experiment.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)
            
        # 3. Generate manifest.json (For the Data Catalog)
        quality_score = 0.0
        if ctx.validation_report:
            quality_score = ctx.validation_report.quality_score
            
        manifest = {
            "experiment_id": ctx.experiment_id,
            "workspace": ctx.workspace,
            "ticker": ctx.ticker,
            "dataset_sha256": ctx.audit.file_hash,
            "quality_score": quality_score,
            "execution_ms": ctx.audit.total_execution_ms,
            "status": ctx.state.value,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        with open(exp_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=4)
            
        logger.info(f"Finalized tracking for {ctx.experiment_id} in workspace '{ctx.workspace}'.")