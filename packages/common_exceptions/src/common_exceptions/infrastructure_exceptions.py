from .base import AppException


class InfrastructureException(AppException):

    error_code = "INFRASTRUCTURE_ERROR"


class DatabaseConnectionError(InfrastructureException):

    error_code = "DB_001"

    retryable = True


class ExternalServiceError(InfrastructureException):

    error_code = "API_001"

    retryable = True


class ConfigurationError(InfrastructureException):

    error_code = "CONFIG_001"

<<<<<<< HEAD
    retryable = False
=======
    retryable = False
>>>>>>> 6cb085790f1e84c507e530b2162f12ed35fe840b
