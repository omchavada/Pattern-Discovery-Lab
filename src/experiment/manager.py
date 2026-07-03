"""
The master orchestrator for quantitative research experiments.
"""

import logging

from src.data_engine.engine import DataEngine
from src.experiment.catalog import DataCatalog
from src.experiment.context import ExperimentContext
from src.experiment.interfaces import BaseRegistry, BaseTracker
from src.experiment.registry import FileRegistry
from src.experiment.state import ExperimentState
from src.experiment.tracker import FileTracker

logger = logging.getLogger(__name__)


class ExperimentManager:
    """
    Coordinates the entire lifecycle of a research experiment with intelligent caching.
    """

    def __init__(
        self, registry: BaseRegistry | None = None, tracker: BaseTracker | None = None
    ) -> None:
        self.registry = registry or FileRegistry()
        self.tracker = tracker or FileTracker()
        self.data_engine = DataEngine()
        logger.info("ExperimentManager initialized with caching enabled.")

    def run_experiment(
        self,
        name: str,
        ticker: str,
        start: str,
        end: str,
        workspace: str = "default",
        tags: dict[str, str] | None = None,
        force_refresh: bool = False,
    ) -> ExperimentContext:
        """
        Executes a complete research pipeline. If identical parameters are found in the catalog,
        it loads the cached data instead of triggering a re-download.
        """
        # --- CACHE INTERCEPTION LAYER ---
        if not force_refresh:
            catalog = DataCatalog()
            query = f"""
                SELECT experiment_id 
                FROM experiments 
                WHERE ticker = '{ticker}' 
                  AND workspace = '{workspace}' 
                  AND start_date = '{start}' 
                  AND end_date = '{end}' 
                  AND status = 'COMPLETED'
                ORDER BY created_at DESC
                LIMIT 1
            """
            cached_result = catalog.query(query)

            if not cached_result.empty:
                exp_id = cached_result.iloc[0]["experiment_id"]
                logger.info(
                    f"CACHE HIT: Pristine data found for {ticker} in "
                    f"{workspace}/{exp_id}. Bypassing pipeline."
                )

                # Rehydrate Context from cache
                ctx = ExperimentContext(
                    workspace=workspace,
                    experiment_id=exp_id,
                    name=name,
                    ticker=ticker,
                    source="Yahoo",
                    start_date=start,
                    end_date=end,
                    state=ExperimentState.COMPLETED,
                )

                # Load the Parquet file back into memory for downstream Feature Engineering
                ctx.market_data = self.tracker.load_artifact(exp_id, "market_data", workspace)
                return ctx

        # --- STANDARD EXECUTION LAYER ---
        exp_id = self.registry.create_experiment(name, tags, workspace=workspace)
        ctx = ExperimentContext(
            workspace=workspace,
            experiment_id=exp_id,
            name=name,
            ticker=ticker,
            source="Yahoo",
            start_date=start,
            end_date=end,
            state=ExperimentState.RUNNING,
        )

        logger.info(f"Starting execution for {exp_id} in {workspace}...")
        ctx = self.data_engine.run_pipeline(ctx, start, end)

        if ctx.market_data is not None:
            ctx.state = ExperimentState.COMPLETED
        else:
            ctx.state = ExperimentState.FAILED

        self.tracker.log_context(ctx)
        return ctx
