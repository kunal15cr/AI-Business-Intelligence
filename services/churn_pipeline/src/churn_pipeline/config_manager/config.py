"""Churn pipeline configuration — merges YAML + env vars into a typed settings object.

Loading priority (highest wins):
    OS env vars  >  .env file  >  {environment}.yaml  >  base.yaml

Usage::

    from churn_pipeline.config_manager.config import get_settings

    settings = get_settings()
    settings.log_resolved_config()   # prints all values, secrets masked
    hp = settings.model_trainer["hyperparameters"]
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from common_config import BaseAppSettings, load_yaml_config

# ── Paths ────────────────────────────────────────────────────────────────

_SERVICE_ROOT = Path(__file__).resolve().parents[3]        # services/churn_pipeline/
_CONFIG_DIR = _SERVICE_ROOT / "configs"
_ENV_FILE = _SERVICE_ROOT / ".env"

print(f"Service root: {_SERVICE_ROOT}")
print(f"Config directory: {_CONFIG_DIR}")
print(f"Environment file: {_ENV_FILE}")


class ChurnSettings(BaseAppSettings):
    """Typed configuration for the churn prediction pipeline.

    Inherits ``BaseAppSettings`` so it automatically picks up
    ``environment``, ``service_name``, ``debug``, and the
    ``log_resolved_config()`` diagnostic method.
    """

    model_config = SettingsConfigDict(
        env_prefix="CHURN_",
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    # ── Pipeline stage configs (loaded from YAML) ────────────────────
    data_ingestion: dict = Field(default_factory=dict)
    data_validation: dict = Field(default_factory=dict)
    model_trainer: dict = Field(default_factory=dict)
    model_evaluation: dict = Field(default_factory=dict)

    # ── Infrastructure ───────────────────────────────────────────────
    mlflow_tracking_uri: str = Field(
        default="http://localhost:5000",
        description="MLflow server URL — overridable via MLFLOW_TRACKING_URI env var.",
    )


@lru_cache(maxsize=1)
def get_settings() -> ChurnSettings:
    """Return the singleton ``ChurnSettings`` instance.

    The ``@lru_cache`` ensures we read YAML and env vars exactly once
    per process.  The returned object is frozen (immutable).
    """
    environment = os.getenv("ENVIRONMENT", "local")

    # Merge base.yaml  ←  {environment}.yaml
    merged_yaml = load_yaml_config(_CONFIG_DIR, environment)

    # Inject the resolved environment so Pydantic picks it up
    merged_yaml.setdefault("environment", environment)

    settings = ChurnSettings(
        **merged_yaml,
        service_name="churn_pipeline",
    )
    settings.log_resolved_config()
    return settings
