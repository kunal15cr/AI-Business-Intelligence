from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

_SERVICE_ROOT = Path(__file__).resolve().parents[3]
_ENV_FILE = _SERVICE_ROOT / ".env"


class ChurnPredictionSettings(BaseSettings):
	"""Settings retained for callers that need the database connection."""

	database_url: SecretStr

	model_config = SettingsConfigDict(
		env_file=str(_ENV_FILE),
		env_file_encoding="utf-8",
		extra="ignore",
	)


churn_prediction_settings = ChurnPredictionSettings()




