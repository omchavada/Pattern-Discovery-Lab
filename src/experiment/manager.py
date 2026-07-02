"""
The master orchestrator for quantitative research experiments.
"""
import logging
from typing import Dict, Any

from src.experiment.interfaces import BaseRegistry, BaseTracker
from src.experiment.registry import FileRegistry
from src.experiment.tracker import FileTracker
from src.experiment.context import ExperimentContext
from src.data_engine.engine import DataEngine

logger = logging.getLogger(__name__)

class ExperimentManager:
    """
    Coordinates the entire lifecycle of a research experiment, 
    from data acquisition to tracking and storage.
    """
    
    def __init__(self, registry: BaseRegistry = None, tracker: BaseTracker = None):
        self.registry = registry or FileRegistry()
        self.tracker = tracker or FileTracker()
        self.data_engine = DataEngine()
        
        logger.info("ExperimentManager initialized.")
        
    def run_experiment(self, name: str, ticker: str, start: str, end: str, workspace: str = "default", tags: Dict[str, str] = None) -> ExperimentContext:
        """Executes a complete research pipeline."""
        
        exp_id = self.registry.create_experiment(name, tags, workspace=workspace)
        from src.experiment.state import ExperimentState
        
        ctx = ExperimentContext(
            workspace=workspace,
            experiment_id=exp_id,
            name=name,
            ticker=ticker,
            source="Yahoo",
            state=ExperimentState.RUNNING
        )
        
        logger.info(f"Starting execution for {exp_id} in {workspace}...")
        
        ctx = self.data_engine.run_pipeline(ctx, start, end)
        
        # If the pipeline returned market data, we assume success for Phase 1
        if ctx.market_data is not None:
            ctx.state = ExperimentState.COMPLETED
        else:
            ctx.state = ExperimentState.FAILED
            
        self.tracker.log_context(ctx)
        return ctx