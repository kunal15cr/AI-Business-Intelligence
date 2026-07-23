from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

class AppException(Exception):
    """Base class for all exceptions in the application."""
    error_code: str = "APP_EXCEPTION"

    retryable: bool = False

    def __init__(
            self,
            message:str,
            *,
            details: dict[str, Any] | None = None,
                 ) -> None:
        
        super().__init__(message)

        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc)
        
    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "error_code": self.error_code,
            "retryable": self.retryable,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        return (
            f"[{self.error_code}] "
            f"{self.message}"
        )
