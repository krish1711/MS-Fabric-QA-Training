# Day 1 setup notebook
# Attach this notebook to the Lakehouse `lh_day1_contoso`
# before running the code.

from pyspark.sql.functions import col, to_date, when

base_path = "Files/day1-lab"

customers_df = (
    spark.read.option("header", True).csv(f"{base_path}/customers.csv")
    .withColumn("IsActive", when(col("IsActive") == "Y", True).otherwise(False))
)

products_df = (
    spark.read.option("header", True).csv(f"{base_path}/products.csv")
    .withColumn("StandardPrice", col("StandardPrice").cast("double"))
)

sales_orders_df = (
    spark.read.option("header", True).csv(f"{base_path}/sales_orders.csv")
    .withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("OrderAmount", col("OrderAmount").cast("double"))
)

customers_df.write.mode("overwrite").format("delta").saveAsTable("customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("products")
sales_orders_df.write.mode("overwrite").format("delta").saveAsTable("sales_orders")

display(
    spark.sql(
        """
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
        UNION ALL
        SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
        UNION ALL
        SELECT 'sales_orders' AS table_name, COUNT(*) AS row_count FROM sales_orders
        """
    )
)
