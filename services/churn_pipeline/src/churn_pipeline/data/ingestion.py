import psycopg

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from common_logging.factory import logger
from common_utility.utility import Utility_functions
from churn_pipeline.exception.data import DataIngestionError
from churn_pipeline.config_manager.settings import churn_prediction_settings


connection_string = churn_prediction_settings.database_url.get_secret_value()

def read_customer_table(table_name):
    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name};")
                customers = cur.fetchall()
                return customers

    except DataIngestionError as e:
        logger.error(f"Error reading table {table_name}: {e}")
        print(f"Error reading table customers: {e}")
        return []

customer_data = read_customer_table("customers")

print(type(customer_data))





