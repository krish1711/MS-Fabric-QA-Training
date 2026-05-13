# Day 2 Bronze notebook
# Attach this notebook to the Lakehouse `lh_day2_contoso_quality`
# before running the code.

from pyspark.sql.functions import col

base_path = "Files/day2-lab"

customers_df = spark.read.option("header", True).csv(f"{base_path}/customers_raw.csv")
products_df = spark.read.option("header", True).csv(f"{base_path}/products_raw.csv")
orders_df = spark.read.option("header", True).csv(f"{base_path}/orders_full_raw.csv")

customers_df.write.mode("overwrite").format("delta").saveAsTable("bronze_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("bronze_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("bronze_orders")

display(
    spark.sql(
        """
        SELECT 'bronze_customers' AS table_name, COUNT(*) AS row_count FROM bronze_customers
        UNION ALL
        SELECT 'bronze_products' AS table_name, COUNT(*) AS row_count FROM bronze_products
        UNION ALL
        SELECT 'bronze_orders' AS table_name, COUNT(*) AS row_count FROM bronze_orders
        """
    )
)
