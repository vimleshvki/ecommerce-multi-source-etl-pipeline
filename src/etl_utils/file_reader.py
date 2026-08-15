import pandas as pd

from .logger import get_logger


logger = get_logger()


def read_orders_from_csv(file_path):
    """
    Extract orders data from CSV file.
    """

    logger.info(f"Reading orders CSV file: {file_path}")

    orders_df = pd.read_csv(file_path)

    logger.info(f"Orders CSV file read successfully. Records: {len(orders_df)}")

    return orders_df


def read_products_from_json(file_path):
    """
    Extract products data from JSON file.
    """

    logger.info(f"Reading products JSON file: {file_path}")

    products_df = pd.read_json(file_path)

    logger.info(f"Products JSON file read successfully. Records: {len(products_df)}")

    return products_df