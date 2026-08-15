import pyodbc

from config import SQL_SERVER_CONNECTION_STRING
from etl_utils.logger import get_logger


logger = get_logger()

#STARTED STATUS
def start_pipeline_audit(pipeline_name):
    """
    Insert a STARTED record into audit table.
    Return generated audit_id.
    """

    connection = None
    cursor = None

    try:
        connection = pyodbc.connect(SQL_SERVER_CONNECTION_STRING)
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO dbo.TABLE_ETL_PIPELINE_RUN_CONTROL (
            PIPELINE_NAME,
            RUN_STATUS,
            START_TIME
        )
        OUTPUT INSERTED.RUN_CTRL_ID
        VALUES (?, 'STARTED', GETDATE());
        """

        cursor.execute(insert_query, pipeline_name)

        RUN_CTRL_ID = cursor.fetchone()[0]

        connection.commit()

        logger.info(f"Audit started. Audit ID: {RUN_CTRL_ID}")

        return RUN_CTRL_ID

    except pyodbc.Error as error_message:
        logger.error(f"Failed to start audit: {error_message}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

#SUCCESS
def update_pipeline_audit_success(
    RUN_CTRL_ID,
    final_report_records,
):
    """
    Update audit table when pipeline succeeds.
    """

    connection = None
    cursor = None

    try:
        connection = pyodbc.connect(SQL_SERVER_CONNECTION_STRING)
        cursor = connection.cursor()

        update_query = """
        UPDATE dbo.TABLE_ETL_PIPELINE_RUN_CONTROL
        SET
            RUN_STATUS = 'SUCCESS',
            END_TIME = GETDATE(),
            RECORDS_LOADED = ?
        WHERE RUN_CTRL_ID = ?;
        """

        cursor.execute(
            update_query,
            final_report_records,
            RUN_CTRL_ID
        )

        connection.commit()

        logger.info(f"Audit updated as SUCCESS. Audit ID: {RUN_CTRL_ID}")

    except pyodbc.Error as error_message:
        logger.error(f"Failed to update success audit: {error_message}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()

#FAILURE
def update_pipeline_audit_failure(RUN_CTRL_ID, error_message):
    """
    Update audit table when pipeline fails.
    """

    connection = None
    cursor = None

    try:
        connection = pyodbc.connect(SQL_SERVER_CONNECTION_STRING)
        cursor = connection.cursor()

        update_query = """
        UPDATE dbo.TABLE_ETL_PIPELINE_RUN_CONTROL
        SET
            RUN_STATUS = 'FAILED',
            END_TIME = GETDATE(),
            ERROR_MESSAGE = ?
        WHERE RUN_CTRL_ID = ?;
        """

        cursor.execute(
            update_query,
            str(error_message),
            RUN_CTRL_ID
        )

        connection.commit()

        logger.info(f"Audit updated as FAILED. Audit ID: {RUN_CTRL_ID}")

    except pyodbc.Error as db_error:
        logger.error(f"Failed to update failure audit: {db_error}")
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()