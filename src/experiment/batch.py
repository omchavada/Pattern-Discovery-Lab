"""
Batch execution engine for parallel experiment runs.
"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from src.experiment.manager import ExperimentManager
from src.experiment.context import ExperimentContext

logger = logging.getLogger(__name__)

class BatchDownloader:
    """
    Orchestrates the parallel execution of multiple data pipelines
    within a specific workspace.
    """
    
    def __init__(self, manager: ExperimentManager = None, max_workers: int = 10):
        self.manager = manager or ExperimentManager()
        self.max_workers = max_workers
        logger.info(f"BatchDownloader initialized with max_workers={self.max_workers}")
        
    def _run_single_safely(self, name: str, ticker: str, start: str, end: str, workspace: str) -> ExperimentContext:
        """Wrapper to ensure an error on one ticker does not crash the entire batch."""
        try:
            return self.manager.run_experiment(
                name=name,
                ticker=ticker,
                start=start,
                end=end,
                workspace=workspace
            )
        except Exception as e:
            logger.error(f"Critical failure in batch worker for {ticker}: {str(e)}")
            # Return a minimal failed context to avoid breaking the collection array
            from src.experiment.state import ExperimentState
            ctx = ExperimentContext(
                workspace=workspace, experiment_id="FAILED", 
                name=name, ticker=ticker, source="Yahoo", state=ExperimentState.FAILED
            )
            ctx.metadata["error"] = str(e)
            return ctx

    def execute_batch(self, tickers: List[str], start: str, end: str, workspace: str) -> List[ExperimentContext]:
        """
        Executes data pipelines for a list of tickers concurrently.
        """
        contexts = []
        total_tickers = len(tickers)
        logger.info(f"Launching batch execution for {total_tickers} tickers in workspace '{workspace}'...")
        
        # Utilize a ThreadPoolExecutor for I/O bound network requests (Yahoo Finance API)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks to the pool
            future_to_ticker = {
                executor.submit(
                    self._run_single_safely, 
                    name=f"Batch Run {ticker}", 
                    ticker=ticker, 
                    start=start, 
                    end=end, 
                    workspace=workspace
                ): ticker for ticker in tickers
            }
            
            # As each download finishes, collect the context object
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    ctx = future.result()
                    contexts.append(ctx)
                    logger.info(f"Batch progress: {len(contexts)}/{total_tickers} finalized ({ticker})")
                except Exception as e:
                    logger.error(f"Thread execution error for {ticker}: {str(e)}")
                    
        return contexts