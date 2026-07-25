from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from churn_pipeline.exception.data import CorruptedDatasetError, DatasetNotFoundError
from churn_pipeline.logging.logging import get_logger

logger = get_logger(__name__)


# Test usage example for logging in this file
def test_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    logger.info("This is a test log from ingestion.py")


