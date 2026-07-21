import sys

from pprint import pprint



from churn_pipeline.exception.base import ChurnException
from churn_pipeline.config_manager.settings import settings


pprint(settings.database_url)

try:
     a= 10 /0
except ChurnException as e:
    pprint(f"Error reading config file: {e}")





