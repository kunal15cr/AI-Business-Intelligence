from packages.common_exceptions.src.base import AppException



class ChurnException(AppException):

    error_code = "CHURN_ERROR"