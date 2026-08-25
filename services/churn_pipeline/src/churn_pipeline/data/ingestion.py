from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from common_logging.factory import logger
from common_utility.utility import Utility_functions


helper = Utility_functions()

helper.load_yaml_file("config.yaml")
logging = logger

logging.info("Starting data ingestion process...")

