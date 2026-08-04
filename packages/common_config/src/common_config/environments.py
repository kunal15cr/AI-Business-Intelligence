"""Environment enum for controlling application behavior across deployment stages."""

from __future__ import annotations

from enum import Enum


class Environment(str, Enum):
    """Supported deployment environments.

    Using ``str`` as a mixin lets Pydantic coerce raw strings from env-vars
    or YAML files directly into the enum (e.g. ``ENVIRONMENT=production``).
    """

    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"

    # ------------------------------------------------------------------
    # Convenience properties used by guard-clauses throughout the app
    # ------------------------------------------------------------------

    @property
    def is_production(self) -> bool:
        """True only in the production environment.

        Use this to gate destructive or irreversible operations:

            if settings.environment.is_production:
                raise RuntimeError("Cannot drop tables in production")
        """
        return self is Environment.PRODUCTION

    @property
    def is_debug_allowed(self) -> bool:
        """Whether verbose / debug-level output is permitted.

        Debug mode is disabled in production to prevent sensitive data
        from leaking into logs or HTTP responses.
        """
        return self is not Environment.PRODUCTION

    def __str__(self) -> str:  # pragma: no cover
        return self.value
