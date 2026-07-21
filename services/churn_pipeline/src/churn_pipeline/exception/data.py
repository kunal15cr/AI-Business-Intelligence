from .base import ChurnException


class DataException(ChurnException):
    pass


class DatasetNotFoundError(DataException):

    error_code = "FILE_001"

    retryable = False


class CorruptedDatasetError(DataException):

    error_code = "FILE_002"

    retryable = False