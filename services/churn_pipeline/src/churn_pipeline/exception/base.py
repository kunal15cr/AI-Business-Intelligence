from common_exceptions.base import AppException


class ChurnException(AppException):

    error_code = "CHURN_ERROR"

print(f"Error reading config file: {ChurnException.error_code}")