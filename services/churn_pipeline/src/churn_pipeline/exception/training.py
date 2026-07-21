from .base import ChurnException


class TrainingException(ChurnException):
    pass


class ModelTrainingError(TrainingException):

    error_code = "TRAIN_001"

    retryable = False