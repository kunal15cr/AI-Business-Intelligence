"""common_config — Production-grade configuration management.

This package provides the shared configuration infrastructure for all
services in the AI Business Intelligence platform.

Quick-start::

    from common_config import BaseAppSettings, Environment, load_yaml_config

    class MyServiceSettings(BaseAppSettings):
        some_param: int = 42

    settings = MyServiceSettings(service_name="my_service")
    settings.log_resolved_config()
"""

from .base_settings import BaseAppSettings
from .environments import Environment
from .yaml_loader import deep_merge, load_yaml_config

__all__ = [
    "BaseAppSettings",
    "Environment",
    "deep_merge",
    "load_yaml_config",
]
