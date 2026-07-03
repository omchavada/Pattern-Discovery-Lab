"""
Core contracts for the Experiment Engine.
"""

import abc
from typing import Any

# (You may need to import ExperimentContext if type checking requires it,
# or use string forward references)


class BaseRegistry(abc.ABC):
    @abc.abstractmethod
    def create_experiment(
        self, name: str, tags: dict[str, str] | None = None, workspace: str = "default"
    ) -> str:
        pass

    @abc.abstractmethod
    def list_experiments(self) -> list[dict[str, Any]]:
        pass


class BaseTracker(abc.ABC):
    @abc.abstractmethod
    def log_artifact(
        self, experiment_id: str, name: str, data: Any, workspace: str = "default"
    ) -> None:
        pass

    @abc.abstractmethod
    def log_metric(self, experiment_id: str, key: str, value: float) -> None:
        pass

    @abc.abstractmethod
    def log_context(self, ctx: Any) -> None:
        pass

    @abc.abstractmethod
    def load_artifact(self, experiment_id: str, name: str, workspace: str = "default") -> Any:
        pass
