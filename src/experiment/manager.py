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
        
    def run_experiment(self, name: str, ticker: str, start: str, end: str, tags: Dict[str, str] = None) -> ExperimentContext:
        """
        Executes a complete research pipeline and logs it as a traceable experiment.
        """
        # 1. Register the Experiment
        exp_id = self.registry.create_experiment(name, tags)
        
        # 2. Initialize the Context
        ctx = ExperimentContext(
            experiment_id=exp_id,
            name=name,
            ticker=ticker,
            source="Yahoo"
        )
        
        logger.info(f"Starting execution for {exp_id}...")
        
        # 3. Execute the Data Phase
        # We pass the context in, and the DataEngine populates it with data and telemetry
        ctx = self.data_engine.run_pipeline(ctx, start, end)
        
        # 4. (Future) Execute Feature Phase
        # 5. (Future) Execute Hypothesis/Backtest Phase
        
        # 6. Track and Save Everything
        self.tracker.log_context(ctx)
        
        logger.info(f"Experiment {exp_id} complete and successfully tracked.")
        return ctx