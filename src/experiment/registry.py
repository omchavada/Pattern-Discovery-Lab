"""
Local file-system implementation of the Experiment Registry.
"""
import os
import glob
import logging
from pathlib import Path
from typing import Dict, Any, List

from src.experiment.interfaces import BaseRegistry
from src.data_engine.config import PROJECT_ROOT

logger = logging.getLogger(__name__)

class FileRegistry(BaseRegistry):
    """
    Manages experiment IDs and directory structures nested within Workspaces.
    """
    
    def __init__(self, base_dir: Path = PROJECT_ROOT / "workspaces"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileRegistry initialized at {self.base_dir}")
        
    def _get_next_experiment_id(self, workspace_path: Path) -> str:
        """Scans the specific workspace directory and increments the highest EXP-XXXX ID."""
        existing_dirs = glob.glob(str(workspace_path / "EXP-*"))
        
        if not existing_dirs:
            return "EXP-000001"
            
        highest_num = 0
        for d in existing_dirs:
            folder_name = os.path.basename(d)
            try:
                num = int(folder_name.split("-")[1])
                highest_num = max(highest_num, num)
            except ValueError:
                continue
                
        next_num = highest_num + 1
        return f"EXP-{next_num:06d}"

    def create_experiment(self, name: str, tags: Dict[str, str] = None, workspace: str = "default") -> str:
        """
        Generates a new Experiment ID inside the specified workspace.
        """
        workspace_path = self.base_dir / workspace
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        exp_id = self._get_next_experiment_id(workspace_path)
        exp_dir = workspace_path / exp_id
        
        exp_dir.mkdir(parents=True, exist_ok=False)
        
        logger.info(f"Created environment: {workspace}/{exp_id} ({name})")
        return exp_id
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        Returns a list of experiments.
        Note: For advanced querying, use the DuckDB DataCatalog instead.
        """
        # We return an empty list here to satisfy the interface.
        # The true indexing power is now handled by src/experiment/catalog.py
        return []