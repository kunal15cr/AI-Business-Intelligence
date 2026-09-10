from pydantic_settings  import BaseSettings, SettingsConfigDict

from .environments import Environment


class BaseAppSettings(BaseSettings):
    """Common settings shared by each service in the platform."""

    service_name: str
    environment: Environment = Environment.LOCAL
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def is_production(self) -> bool:
        """Return whether the service is running in production."""
        return self.environment is Environment.PRODUCTION

    def log_resolved_config(self) -> None:
        """Log the resolved settings without exposing secret values."""
        print(f"Resolved settings for {self.service_name}: {self.model_dump()}")


# Backward-compatible name for code that imported Settings directly.
Settings = BaseAppSettings


