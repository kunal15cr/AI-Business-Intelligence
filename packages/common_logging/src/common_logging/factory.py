import logging
import os
from datetime import datetime
from typing import Any



def _default_log_path() -> str:
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
    return os.path.join(log_dir, f"{timestamp}.log")


def configure_logging(level: int | str = logging.INFO, log_file_path: str | None = None) -> None:
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    if logging.getLogger().handlers:
        return

    LOG_FILE_PATH = log_file_path or _default_log_path()
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    logging.basicConfig(
        level=level,
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH, mode="w"),
            logging.StreamHandler(),
        ],
        force=True,
    )


def get_logger(name: str | None = None) -> logging.Logger:
    configure_logging()
    logger_instance = logging.getLogger(name or __name__)
    return logger_instance


logger = get_logger(__name__)