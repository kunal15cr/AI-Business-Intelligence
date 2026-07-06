from common_config.environment import Environment
def build_logging_config(env: Environment) -> dict:
    formatter = "json" if env.is_production else "console"
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "console": {"format": "%(asctime)s %(levelname)s [%(name)s]: %(message)s"},
        },
        "handlers": {"default": {"class": "logging.StreamHandler", "formatter": formatter}},
        "root": {"handlers": ["default"], "level": "INFO"},
    }
