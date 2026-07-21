from .base import ChurnException


class ValidationException(ChurnException):
    pass


class SchemaValidationError(ValidationException):

    error_code = "VALIDATION_001"