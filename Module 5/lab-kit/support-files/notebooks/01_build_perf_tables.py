# Day 5 pipeline build notebook
# Attach this notebook to the Lakehouse `lh_day5_contoso_runtime`
# before running the code.

from pyspark.sql.functions import col, count as spark_count, sum as spark_sum

base_path = "Files/day5-lab"

customers_df = spark.read.option("header", True).csv(f"{base_path}/customers.csv")
products_df = spark.read.option("header", True).csv(f"{base_path}/products.csv")
orders_df = spark.read.option("header", True).csv(f"{base_path}/orders.csv")

customers_df = customers_df.select(
    col("CustomerID"),
    col("CustomerName"),
    col("Region"),
    col("CustomerSegment"),
    col("IsActive"),
)

products_df = products_df.select(
    col("ProductID"),
    col("ProductName"),
    col("Category"),
    col("UnitPrice").cast("decimal(18,2)").alias("UnitPrice"),
    col("IsActive"),
)

orders_df = orders_df.select(
    col("OrderID"),
    col("OrderDate").cast("date").alias("OrderDate"),
    col("CustomerID"),
    col("ProductID"),
    col("Quantity").cast("int").alias("Quantity"),
    col("UnitPrice").cast("decimal(18,2)").alias("UnitPrice"),
    col("OrderAmount").cast("decimal(18,2)").alias("OrderAmount"),
    col("OrderStatus"),
)

customers_df.write.mode("overwrite").format("delta").saveAsTable("perf_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("perf_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("perf_orders")

summary_df = (
    orders_df.join(customers_df, "CustomerID", "inner")
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").cast("decimal(18,2)").alias("TotalSales"),
    )
    .orderBy("Region")
)

summary_df.write.mode("overwrite").format("delta").saveAsTable("perf_region_sales_summary")

display(
    spark.sql(
        """
        SELECT 'perf_customers' AS table_name, COUNT(*) AS row_count FROM perf_customers
        UNION ALL
        SELECT 'perf_products' AS table_name, COUNT(*) AS row_count FROM perf_products
        UNION ALL
        SELECT 'perf_orders' AS table_name, COUNT(*) AS row_count FROM perf_orders
        UNION ALL
        SELECT 'perf_region_sales_summary' AS table_name, COUNT(*) AS row_count FROM perf_region_sales_summary
        """
    )
)
