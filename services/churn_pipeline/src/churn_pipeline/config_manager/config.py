import os, yaml
from pathlib import Path
from functools import lru_cache
from pydantic_settings import SettingsConfigDict
from common_config.base_settings import BaseAppSettings

CONFIG_DIR = Path(__file__).parents[2] / "configs"

def _merged() -> dict:
    env = os.getenv("ENVIRONMENT", "local")
    return yaml.safe_load((CONFIG_DIR / "base.yaml").read_text()) or {}

class ChurnSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="CHURN_")
    data_ingestion: dict = {}
    data_validation: dict = {}
    model_trainer: dict = {}
    model_evaluation: dict = {}
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

@lru_cache
def get_settings() -> ChurnSettings:
    return ChurnSettings(**_merged(), service_name="churn_pipeline")
