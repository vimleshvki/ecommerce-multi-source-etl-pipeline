from .logger import get_logger


logger = get_logger()


def validate_orders(orders_df):
    """
    Validate raw orders data.
    """

    logger.info("Starting order validation")

    raw_orders_df = orders_df.copy() #duplicate the DF

    raw_orders_df["rejection_reason"] = ""

    raw_orders_df.loc[
        raw_orders_df["order_id"].isna(),
        "rejection_reason"
    ] = "Missing order_id"

    raw_orders_df.loc[
        raw_orders_df["customer_id"].isna(),
        "rejection_reason"
    ] = "Missing customer_id"

    raw_orders_df.loc[
        raw_orders_df["product_id"].isna(),
        "rejection_reason"
    ] = "Missing product_id"

    raw_orders_df.loc[
        raw_orders_df["quantity"] <= 0,
        "rejection_reason"
    ] = "Quantity must be greater than 0"

    raw_orders_df.loc[
        raw_orders_df["unit_price"] < 0,
        "rejection_reason"
    ] = "Unit price cannot be negative"

    raw_orders_df.loc[
        (raw_orders_df["discount"] < 0) | (raw_orders_df["discount"] > 100),
        "rejection_reason"
    ] = "Discount must be between 0 and 100"

    valid_orders_df = raw_orders_df[ #boolean filtering
        raw_orders_df["rejection_reason"] == ""
    ].copy()

    rejected_orders_df = raw_orders_df[
        raw_orders_df["rejection_reason"] != ""
    ].copy()

    logger.info(f"Validation completed. Valid records: {len(valid_orders_df)}")
    logger.info(f"Validation completed. Rejected records: {len(rejected_orders_df)}")
    #raise Exception("Intentional failure during validation step")
    return valid_orders_df, rejected_orders_df