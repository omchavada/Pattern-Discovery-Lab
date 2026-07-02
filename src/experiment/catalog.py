"""
The Data Catalog powered by DuckDB. 
Indexes all experiment manifests for instant cross-sectional querying.
"""
import logging
import duckdb
import pandas as pd
from pathlib import Path

from src.data_engine.config import PROJECT_ROOT

logger = logging.getLogger(__name__)

class DataCatalog:
    """
    Provides a searchable SQL interface over all research experiments.
    """
    
    def __init__(self, workspaces_dir: Path = PROJECT_ROOT / "workspaces"):
        self.workspaces_dir = workspaces_dir
        # Spin up an in-memory DuckDB instance
        self.conn = duckdb.connect(database=':memory:')
        logger.info("DuckDB Data Catalog initialized.")
        
    def _get_manifest_glob(self) -> str:
        """Returns the glob pattern to find all manifests."""
        # e.g., /path/to/workspaces/*/*/manifest.json
        return str(self.workspaces_dir / "*" / "*" / "manifest.json")

    def query(self, sql_query: str) -> pd.DataFrame:
        """
        Executes a raw SQL query against the virtual manifest table.
        The virtual table is named 'experiments'.
        """
        glob_path = self._get_manifest_glob()
        
        # Inject the DuckDB read_json_auto function as a CTE (Common Table Expression)
        # This makes the user's SQL query incredibly clean.
        injected_sql = f"""
        WITH experiments AS (
            SELECT * FROM read_json_auto('{glob_path}')
        )
        {sql_query}
        """
        
        try:
            return self.conn.execute(injected_sql).df()
        except duckdb.IOException:
            # Handles the case where no manifests exist yet
            logger.warning("No manifests found in workspaces.")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Catalog query failed: {str(e)}")
            raise

    def get_all_experiments(self) -> pd.DataFrame:
        """Returns the entire catalog as a DataFrame."""
        return self.query("SELECT * FROM experiments ORDER BY created_at DESC")
        
    def get_best_datasets(self, min_score: float = 95.0) -> pd.DataFrame:
        """Finds highly validated datasets ready for feature engineering."""
        return self.query(f"""
            SELECT experiment_id, workspace, ticker, quality_score, dataset_sha256
            FROM experiments 
            WHERE status = 'COMPLETED' AND quality_score >= {min_score}
            ORDER BY quality_score DESC
        """)