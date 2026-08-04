"""Database and secrets settings for the churn pipeline.

Separating secret-bearing settings from pipeline config keeps
responsibilities clear:

- ``config.py``   → YAML-driven pipeline parameters (data paths, hyperparams)
- ``settings.py`` → Infrastructure secrets (database URL, API keys)
"""

from __future__ import annotations

from pathlib import Path

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import SettingsConfigDict

from common_config import BaseAppSettings

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class SecretSettings(BaseAppSettings):
    """Infrastructure secrets for the churn pipeline.

    ``SecretStr`` ensures the raw database URL is never accidentally
    printed in logs, ``repr()`` output, or error messages.
    """

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    database_url: SecretStr = Field(
        validation_alias=AliasChoices(
            "DATABASE_URL",
            "database_url",
        ),
        description="PostgreSQL connection string (Neon, Supabase, etc.)",
    )


# Module-level singleton — created at import time.
# Use ``secret_settings.database_url.get_secret_value()`` to access the raw URL.
secret_settings = SecretSettings(service_name="churn_pipeline")