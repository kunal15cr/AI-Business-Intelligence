import logging.config
import structlog
import os
from .processors import make_redactor, correlation_id_var

def get_logger(name: str):
    """Factory to get a hierarchical logger for a specific module."""
    return structlog.get_logger(name)

def configure_logging(
    service_name: str, 
    level: str = "INFO", 
    enable_file_logging: bool = False,
    log_file_path: str = "logs/app.log",
    extra_redaction_keys: set = None
):
    """Configures dual-output logging: colored console + JSON rotating file."""
    
    # 1. Processors applied to EVERY log line (Context, Timestamps, Redaction)
    shared_processors = [
        structlog.contextvars.merge_contextvars,      # Injects correlation_id[cite: 9]
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),  # ISO-8601 timestamps[cite: 9]
        make_redactor(extra_redaction_keys),          # Redacts PII[cite: 9]
    ]

    # 2. Configure structlog to pass events to standard library logging
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 3. Define standard logging configuration (dictConfig)[cite: 9]
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [structlog.dev.ConsoleRenderer(colors=True)],
            },
            "json_formatter": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [structlog.processors.JSONRenderer()],
            },
