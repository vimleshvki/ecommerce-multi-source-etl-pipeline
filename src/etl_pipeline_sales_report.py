from config import (
    ORDERS_CSV_FILE,
    PRODUCTS_JSON_FILE,
    FINAL_REPORT_FILE,
    REJECTED_ORDERS_FILE
)

from etl_utils import (
    get_logger,
    read_orders_from_csv,
    read_products_from_json,
    validate_orders,
    merge_extracted_data,
    apply_business_transformations,
    load_final_report_to_sql,
    start_pipeline_audit,
    update_pipeline_audit_success,
    update_pipeline_audit_failure
)

logger = get_logger()

def run_ecommerce_etl_pipeline():
    RUN_CTRL_ID = None

    try:
        logger.info("Starting E-commerce Multi-Source ETL Pipeline")

        RUN_CTRL_ID = start_pipeline_audit(
            "ecommerce_multi_source_etl_pipeline"
        )

        logger.info("Step 1: Extracting orders from CSV")
        orders_df = read_orders_from_csv(ORDERS_CSV_FILE)

        logger.info("Step 2: Extracting products from JSON")
        products_df = read_products_from_json(PRODUCTS_JSON_FILE)

        logger.info("Step 4: Cleaning and validating orders")
        valid_orders_df, rejected_orders_df = validate_orders(orders_df)

        logger.info("Step 5: Merging extracted data using Pandas")
        merged_df = merge_extracted_data(
            valid_orders_df,
            products_df
            #customers_df
        )
        #transformation.
        logger.info("Step 6: Applying business transformations")
        final_report_df = apply_business_transformations(merged_df)

        logger.info("Step 7: Saving final reporting dataset as CSV")
        final_report_df.to_csv(FINAL_REPORT_FILE, index=False)

        logger.info("Step 8: Saving rejected orders as CSV")
        rejected_orders_df.to_csv(REJECTED_ORDERS_FILE, index=False)

        logger.info("Step 9: Loading final reporting dataset into SQL Server")
        print(final_report_df)
        load_final_report_to_sql(final_report_df)

        update_pipeline_audit_success(
            RUN_CTRL_ID=RUN_CTRL_ID,
            final_report_records=len(final_report_df)
        )

        logger.info("ETL Pipeline completed successfully")

    except Exception as error_message:
        logger.error(f"ETL Pipeline failed: {error_message}")

        if RUN_CTRL_ID is not None:
            update_pipeline_audit_failure(
                RUN_CTRL_ID=RUN_CTRL_ID,
                error_message=error_message
            )

        raise  #re-raise the same exception

if __name__ == "__main__":
    run_ecommerce_etl_pipeline()