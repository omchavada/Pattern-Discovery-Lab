"""
Core contracts for the Experiment Engine.
"""
import abc
from typing import Dict, Any, List

class BaseRegistry(abc.ABC):
    """
    Contract for generating experiment IDs and querying past experiments.
    """
    
    @abc.abstractmethod
    def create_experiment(self, name: str, tags: Dict[str, str]) -> str:
        """Generates a unique ID (e.g., EXP-000001) and initializes storage."""
        pass
        
    @abc.abstractmethod
    def list_experiments(self) -> List[Dict[str, Any]]:
        """Returns a searchable list of past experiments."""
        pass

class BaseTracker(abc.ABC):
    """
    Contract for logging artifacts, metrics, and state during an experiment.
    """
    
    @abc.abstractmethod
    def log_artifact(self, experiment_id: str, name: str, data: Any) -> None:
        """Saves a file/dataframe to the experiment's isolated folder."""
        pass
        
    @abc.abstractmethod
    def log_metric(self, experiment_id: str, key: str, value: float) -> None:
        """Logs a numerical result (e.g., Sharpe Ratio = 1.72)."""
        pass
    