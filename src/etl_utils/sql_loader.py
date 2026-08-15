import pandas as pd
import pyodbc

from config import SQL_SERVER_CONNECTION_STRING
from .logger import get_logger


logger = get_logger()


def load_final_report_to_sql(final_report_df):
    """
    Load final reporting dataset into SQL Server table.
    """

    connection = None
    cursor = None

    try:
        logger.info("Connecting to SQL Server for final report load")

        connection = pyodbc.connect(SQL_SERVER_CONNECTION_STRING)
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO dbo.TABLE_FINAL_SALES_REPORT (
            ORDER_ID,
            ORDER_DATE,
            CUSTOMER_ID,
            PRODUCT_ID,
            PRODUCT_NAME,
            CATEGORY,
            GST_AMOUNT,
            FINAL_AMOUNT,
            PAYMENT_METHOD,
            CITY,
            COUNTRY,
            ORDER_VALUE_CATEGORY
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        columns_to_insert = [
            "order_id",
            "order_date",
            "customer_id",
            "product_id",
            "product_name",
            "category",
            "gst_amount",
            "final_amount",           
            "payment_method",
            "city",
            "country",
            "order_value_category"
        ]

        final_report_df = final_report_df.where(
            pd.notnull(final_report_df),
            None
        )

        records_to_insert = final_report_df[columns_to_insert].values.tolist()

        cursor.fast_executemany = True
        cursor.executemany(insert_query, records_to_insert)

        connection.commit()

        logger.info(f"Final report loaded into SQL Server. Records: {len(records_to_insert)}")

    except pyodbc.Error as error_message:
        logger.error(f"Database error while loading final report: {error_message}")

        if connection is not None:
            connection.rollback()
            logger.info("Transaction rolled back for final report load")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

        logger.info("SQL Server connection closed for final report load")


