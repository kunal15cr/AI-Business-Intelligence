# packages/common_config/src/common_config/logger.py

import logging
import uuid
from contextvars import ContextVar
from typing import Any, Dict


correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="system")
customer_id_var: ContextVar[str | None] = ContextVar("customer_id", default=None)

class ContextFilter(logging.Filter):
    """
    Injects global context variables (like correlation_id) into every log record.
    This ensures every log line across microservices can be tied to a single run.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get()
        
        # Only inject customer_id if it exists in the current context
        customer_id = customer_id_var.get()
        if customer_id:
            record.customer_id = customer_id
            
        return True

def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a logger configured with the ContextFilter.
    Use this instead of standard `logging.getLogger(__name__)`.
    """
    logger = logging.getLogger(name)
    
    # Avoid attaching multiple filters if the logger is retrieved multiple times
    if not any(isinstance(f, ContextFilter) for f in logger.filters):
        logger.addFilter(ContextFilter())
        
    return logger

def set_correlation_id(new_id: str | None = None) -> str:
    """Sets a new correlation ID for the current context and returns it."""
    cid = new_id or str(uuid.uuid4())
    correlation_id_var.set(cid)
    return cid

def set_customer_context(customer_id: str) -> None:
    """Sets the customer ID in the current logging context."""
    customer_id_var.set(customer_id)