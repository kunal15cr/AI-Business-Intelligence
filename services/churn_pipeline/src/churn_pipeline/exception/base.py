from common_exceptions.base import AppException


class ChurnException(AppException):
    """Base exception type for churn pipeline errors."""

    error_code = "CHURN_ERROR"