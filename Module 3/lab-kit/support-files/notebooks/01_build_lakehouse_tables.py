# Day 3 Lakehouse base notebook
# Attach this notebook to the Lakehouse `lh_day3_contoso`
# before running the code.

from pyspark.sql.functions import col, to_date

base_path = "Files/day3-lab"

customers_df = spark.read.option("header", True).csv(f"{base_path}/customers.csv")
products_df = (
    spark.read.option("header", True).csv(f"{base_path}/products.csv")
    .withColumn("StandardPrice", col("StandardPrice").cast("double"))
)
orders_df = (
    spark.read.option("header", True).csv(f"{base_path}/orders_base.csv")
    .withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("OrderAmount", col("OrderAmount").cast("double"))
)

customers_df.write.mode("overwrite").format("delta").saveAsTable("lake_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("lake_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("lake_orders")

display(
    spark.sql(
        """
        SELECT 'lake_customers' AS table_name, COUNT(*) AS row_count FROM lake_customers
        UNION ALL
        SELECT 'lake_products' AS table_name, COUNT(*) AS row_count FROM lake_products
        UNION ALL
        SELECT 'lake_orders' AS table_name, COUNT(*) AS row_count FROM lake_orders
        """
    )
)
