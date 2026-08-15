def merge_extracted_data(valid_orders_df, products_df):
    """
    Merge orders, products, and customers data.
    """

    orders_products_df = valid_orders_df.merge(
        products_df,
        on="product_id",
        how="left"
    )

    #final_merged_df = orders_products_df.merge(
        #customers_df,
        #on="customer_id",
        #how="left"
    #)

    return orders_products_df


def apply_business_transformations(merged_df):
    """
    Apply business calculations and create final reporting columns.
    """

    transformed_df = merged_df.copy()

    transformed_df["order_date"] = transformed_df["order_date"].astype(str)

    transformed_df["gross_amount"] = (
        transformed_df["quantity"] * transformed_df["unit_price"]
    )

    transformed_df["discount_amount"] = (
        transformed_df["gross_amount"] * transformed_df["discount"] / 100
    )

    transformed_df["amount_after_discount"] = (
        transformed_df["gross_amount"] - transformed_df["discount_amount"]
    )

    transformed_df["gst_amount"] = (
        transformed_df["amount_after_discount"] * 0.18
    )

    transformed_df["final_amount"] = (
        transformed_df["amount_after_discount"] + transformed_df["gst_amount"]
    )

    transformed_df["order_value_category"] = transformed_df["final_amount"].apply(
        lambda amount: "High Value" if amount >= 20000 else "Normal Value"
    )

    final_columns = [
        "order_id",
        "order_date",
        "customer_id",
        #"customer_name",
        #"customer_segment",
        "product_id",
        "product_name",
        "category",
        "brand",
        "quantity",
        "unit_price",
        "discount",
        "gross_amount",
        "discount_amount",
        "amount_after_discount",
        "gst_amount",
        "final_amount",
        "payment_method",
        "city",
        "country",
        "order_value_category"
    ]

    final_report_df = transformed_df[final_columns]

    return final_report_df