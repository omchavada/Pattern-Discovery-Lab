"""
Global settings management for Pattern Discovery Lab.
Loads environment-specific configurations from YAML files.
"""

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass
class Settings:
    environment: str
    data_root: Path
    workspace_root: Path
    db_path: Path
    max_retries: int
    timeout_seconds: int
    max_workers: int


def load_settings(env: str = "development") -> Settings:
    """Loads the active configuration based on the environment."""
    config_path = PROJECT_ROOT / "configs" / f"{env}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    return Settings(
        environment=raw_config.get("environment", "development"),
        data_root=PROJECT_ROOT / raw_config["paths"]["data_root"],
        workspace_root=PROJECT_ROOT / raw_config["paths"]["workspace_root"],
        db_path=PROJECT_ROOT
        / raw_config["paths"]["data_root"]
        / "database"
        / raw_config["paths"]["database_name"],
        max_retries=raw_config["engine"]["max_retries"],
        timeout_seconds=raw_config["engine"]["timeout_seconds"],
        max_workers=raw_config["batch"]["max_workers"],
    )


# The global settings instance
SETTINGS = load_settings(os.getenv("PDL_ENV", "development"))
