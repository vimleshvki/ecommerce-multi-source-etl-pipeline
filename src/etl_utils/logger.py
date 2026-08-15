import logging
import os

from config import LOG_FILE

"""
logging.getLogger()    → creates logger object
logger.setLevel()      → decides what level of logs to capture
FileHandler()          → writes logs to file
Formatter()            → controls log message format
logger.addHandler()    → attaches file handler to logger
"""


def get_logger():
    """
    Create and return logger object for ETL pipeline.
    Logs will be written to logs/etl_pipeline.log file.
    """

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("ecommerce_etl_logger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
    