from common_exceptions.base import AppException



class ChurnException(AppException):

    error_code = "CHURN_ERROR"

