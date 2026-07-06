from pydantic_settings import BaseSettings, SettingsConfigDict
from common_config.environment import Environment
class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    environment: Environment = Environment.LOCAL
    service_name: str
    log_level: str = "INFO"
