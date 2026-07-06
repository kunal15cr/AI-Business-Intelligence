# packages/common_config/src/common_config/exceptions.py

from typing import Any, Dict, Optional

class CIPBaseException(Exception):
    """
    Base exception for all Custom AI Platform (CIP) errors.
    Allows global error handlers to catch domain-specific errors predictably.
    """
    def __init__(
        self, 
        message: str, 
        error_code: str = "INTERNAL_ERROR", 
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.payload = payload or {}

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message} (Payload: {self.payload})"

# --- Data Domain Exceptions ---

class DataValidationError(CIPBaseException):
    """Raised when ingested data fails schema checks (e.g., missing columns)."""
    def __init__(self, message: str, missing_columns: list[str]):
        super().__init__(
            message=message,
            error_code="DATA_VALIDATION_FAILED",
            status_code=422,
            payload={"missing_columns": missing_columns}
        )

# --- Machine Learning Domain Exceptions ---

class ModelNotTrainedError(CIPBaseException):
    """Raised when trying to run inference on a model that hasn't been fitted."""
    def __init__(self, model_name: str):
        super().__init__(
            message=f"The model '{model_name}' has not been trained yet.",
            error_code="MODEL_NOT_TRAINED",
            status_code=400,
            payload={"model_name": model_name}
            
        )

# In packages/common_config/src/common_config/exceptions.py

class DataIngestionError(CIPBaseException):
    """Raised when source data cannot be found, read, or parsed."""
    def __init__(self, message: str, filepath_or_query: str):
        super().__init__(
            message=message,
            error_code="DATA_INGESTION_FAILED",
            status_code=500,
            payload={"source": filepath_or_query}
        )

class DataDriftDetectedError(CIPBaseException):
    """Raised when production inference data diverges significantly from training data."""
    def __init__(self, drift_score: float, threshold: float):
        super().__init__(
            message="Data drift threshold exceeded. Model predictions may be unreliable.",
            error_code="DATA_DRIFT_DETECTED",
            status_code=409,
            payload={"drift_score": drift_score, "threshold": threshold}
        )

# --- Agentic/LLM Exceptions ---

class LLMProviderTimeoutError(CIPBaseException):
    """Raised when OpenAI or Anthropic takes too long to respond to the Agent."""
    def __init__(self, provider: str, timeout_seconds: int):
        super().__init__(
            message=f"LLM Provider {provider} timed out after {timeout_seconds}s.",
            error_code="LLM_TIMEOUT",
            status_code=504,
            payload={"provider": provider}
        )