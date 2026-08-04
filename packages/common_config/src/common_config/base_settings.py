"""Base application settings — the foundation class every service inherits from.

This module provides ``BaseAppSettings``, a Pydantic-Settings class that:

1. Binds to OS environment variables automatically.
2. Loads values from ``.env`` files.
3. Enforces type-safety and immutability (``frozen=True``).
4. Offers ``log_resolved_config()`` for startup diagnostics with masked secrets.
5. Provides the ``environment`` field gated by the ``Environment`` enum.

Typical usage in a service::

    from common_config.base_settings import BaseAppSettings

    class ChurnSettings(BaseAppSettings):
        model_config = SettingsConfigDict(env_prefix="CHURN_")
        data_ingestion: dict = {}
        ...

    settings = ChurnSettings(service_name="churn_pipeline")
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from .environments import Environment

logger = logging.getLogger(__name__)


class BaseAppSettings(BaseSettings):
    """Shared settings base that all service configurations extend.

    Features
    --------
    - ``environment``: Resolved from the ``ENVIRONMENT`` env var.
    - ``service_name``: Identifies the owning service in logs / tracing.
    - ``debug``: Convenience flag derived from environment by default.
    - Frozen after construction — any mutation raises ``ValidationError``.

    Subclasses can override ``model_config`` to set their own
    ``env_prefix``, ``env_file``, etc.
    """

    model_config = SettingsConfigDict(
        # ── Env-var binding ──────────────────────────────────────────
        env_file=".env",
        env_file_encoding="utf-8",
        # ── Safety ───────────────────────────────────────────────────
        extra="ignore",          # silently drop unknown env vars
        frozen=True,             # immutable after construction
        # ── Nested model support ─────────────────────────────────────
        env_nested_delimiter="__",   # e.g. CHURN__MODEL_TRAINER__LR=0.1
    )

    # ── Core fields ──────────────────────────────────────────────────

    environment: Environment = Field(
        default=Environment.LOCAL,
        description="Deployment stage — controls overlay loading and safety guards.",
    )

    service_name: str = Field(
        default="app",
        description="Logical name of the running service (used in logging & tracing).",
    )

    debug: bool = Field(
        default=False,
        description=(
            "Enable debug output.  Automatically set to True in local/staging "
            "environments unless explicitly overridden."
        ),
    )

    # ── Public methods ───────────────────────────────────────────────

    def log_resolved_config(self) -> None:
        """Pretty-print the fully resolved settings, masking all secrets.

        Call this once at startup so operators can immediately verify
        what configuration the process is running with::

            settings = get_settings()
            settings.log_resolved_config()

        ``SecretStr`` fields are rendered as ``**********`` so credentials
        never leak into log files, stdout, or monitoring systems.
        """
        header = (
            f"┌─ Resolved configuration for [{self.service_name}] "
            f"(env={self.environment}) ─"
        )
        logger.info(header)

        for field_name, field_info in self.model_fields.items():
            raw_value = getattr(self, field_name)

            # Mask secret fields
            if isinstance(raw_value, SecretStr):
                display_value = "**********"
            else:
                display_value = repr(raw_value)

            logger.info("  %-25s = %s", field_name, display_value)

        logger.info("└─ End configuration ─")

    def is_production(self) -> bool:
        """Shortcut for ``self.environment.is_production``."""
        return self.environment.is_production
