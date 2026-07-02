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
    Manages experiment IDs and directory structures on the local disk.
    """
    
    def __init__(self, base_dir: Path = PROJECT_ROOT / "experiments"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileRegistry initialized at {self.base_dir}")
        
    def _get_next_experiment_id(self) -> str:
        """Scans the directory and increments the highest EXP-XXXX ID."""
        existing_dirs = glob.glob(str(self.base_dir / "EXP-*"))
        
        if not existing_dirs:
            return "EXP-000001"
            
        # Extract the integer part of the folder names and find the max
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

    def create_experiment(self, name: str, tags: Dict[str, str] = None) -> str:
        """
        Generates a new Experiment ID and initializes its isolated folder.
        """
        exp_id = self._get_next_experiment_id()
        exp_dir = self.base_dir / exp_id
        
        # Create the master experiment directory
        exp_dir.mkdir(parents=True, exist_ok=False)
        
        logger.info(f"Created new experiment environment: {exp_id} ({name})")
        return exp_id

    def list_experiments(self) -> List[Dict[str, Any]]:
        """
        (Placeholder for future sprint) Will return a parsed list of all past experiments.
        """
        pass