# Day 4 pipeline notebook
# Attach this notebook to the Lakehouse `lh_day4_contoso_ops`
# before running the code.

from pyspark.sql.functions import col, count as spark_count, sum as spark_sum

base_path = "Files/day4-lab"

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

customers_df.write.mode("overwrite").format("delta").saveAsTable("stg_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("stg_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("stg_orders")

summary_df = (
    orders_df.join(customers_df, "CustomerID", "inner")
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").cast("decimal(18,2)").alias("TotalSales"),
    )
    .orderBy("Region")
)

summary_df.write.mode("overwrite").format("delta").saveAsTable("qa_region_sales_summary")

display(
    spark.sql(
        """
        SELECT 'stg_customers' AS table_name, COUNT(*) AS row_count FROM stg_customers
        UNION ALL
        SELECT 'stg_products' AS table_name, COUNT(*) AS row_count FROM stg_products
        UNION ALL
        SELECT 'stg_orders' AS table_name, COUNT(*) AS row_count FROM stg_orders
        UNION ALL
        SELECT 'qa_region_sales_summary' AS table_name, COUNT(*) AS row_count FROM qa_region_sales_summary
        """
    )
)

display(spark.sql("SELECT * FROM qa_region_sales_summary ORDER BY Region"))
