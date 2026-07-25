from __future__ import annotations

import logging
import logging.handlers
import uuid
from contextvars import ContextVar
from pathlib import Path
from typing import Any

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="system")
customer_id_var: ContextVar[str | None] = ContextVar("customer_id", default=None)


class ContextFilter(logging.Filter):
    """Attach request-scoped correlation metadata to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        customer_id = customer_id_var.get()
        if customer_id:
            record.customer_id = customer_id
        return True


def _default_formatter() -> logging.Formatter:
    return logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(correlation_id)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


def configure_logging(
    service_name: str = "churn_pipeline",
    level: str = "INFO",
    enable_file_logging: bool = True,
    log_file_path: str | Path = "logs/churn_pipeline.log",
) -> None:
    """Configure a production-friendly logger once for the service.

    - console handler for operator visibility
    - rotating file handler for persistence
    - context filter to include correlation id in every record
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())

    if root_logger.handlers:
        return

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.upper())
    console_handler.setFormatter(_default_formatter())
    console_handler.addFilter(ContextFilter())

    root_logger.addHandler(console_handler)

    if enable_file_logging:
        file_path = Path(log_file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(level.upper())
        file_handler.setFormatter(_default_formatter())
        file_handler.addFilter(ContextFilter())
        root_logger.addHandler(file_handler)

    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Return a named logger with the shared context-aware configuration."""
    configure_logging()

    logger = logging.getLogger(name)
    logger.setLevel(logging.getLogger().level)
    logger.propagate = False

    if not any(isinstance(filter_obj, ContextFilter) for filter_obj in logger.filters):
        logger.addFilter(ContextFilter())

    return logger


def set_correlation_id(new_id: str | None = None) -> str:
    """Set a correlation ID for the current context and return it."""
    cid = new_id or str(uuid.uuid4())
    correlation_id_var.set(cid)
    return cid


def set_customer_context(customer_id: str) -> None:
    """Set the customer ID in the current logging context."""
    customer_id_var.set(customer_id)
