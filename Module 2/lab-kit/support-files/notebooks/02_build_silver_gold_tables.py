# Day 2 Silver and Gold notebook
# Attach this notebook to the Lakehouse `lh_day2_contoso_quality`
# before running the code.

from pyspark.sql.functions import col, lit, to_date, trim, row_number, sum as spark_sum, count as spark_count, when
from pyspark.sql.window import Window

customers = (
    spark.table("bronze_customers")
    .select(
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("CustomerName")).alias("CustomerName"),
        trim(col("Region")).alias("Region"),
        trim(col("CustomerType")).alias("CustomerType"),
        trim(col("IsActive")).alias("IsActive"),
    )
    .filter(col("Region").isNotNull() & (col("Region") != ""))
)

products = (
    spark.table("bronze_products")
    .select(
        trim(col("ProductID")).alias("ProductID"),
        trim(col("ProductName")).alias("ProductName"),
        trim(col("Category")).alias("Category"),
        col("StandardPrice").cast("double").alias("StandardPrice"),
    )
    .filter(col("Category").isNotNull() & (col("Category") != ""))
)

raw_orders = (
    spark.table("bronze_orders")
    .select(
        trim(col("OrderID")).alias("OrderID"),
        to_date(col("OrderDate"), "yyyy-MM-dd").alias("OrderDate"),
        trim(col("CustomerID")).alias("CustomerID"),
        trim(col("ProductID")).alias("ProductID"),
        col("Quantity").cast("int").alias("Quantity"),
        col("UnitPrice").cast("double").alias("UnitPrice"),
        col("OrderAmount").cast("double").alias("OrderAmount"),
        trim(col("OrderStatus")).alias("OrderStatus"),
    )
)

valid_statuses = ["Shipped", "Processing", "Cancelled"]

order_window = Window.partitionBy("OrderID").orderBy(col("OrderDate").asc())
orders_with_rank = raw_orders.withColumn("dup_rank", row_number().over(order_window))

joined_orders = (
    orders_with_rank.alias("o")
    .join(customers.select("CustomerID", "Region").alias("c"), col("o.CustomerID") == col("c.CustomerID"), "left")
    .join(products.select("ProductID").alias("p"), col("o.ProductID") == col("p.ProductID"), "left")
)

silver_order_rejections = (
    joined_orders
    .where(
        (col("o.CustomerID").isNull()) |
        (col("o.CustomerID") == "") |
        col("c.CustomerID").isNull() |
        col("p.ProductID").isNull() |
        (~col("o.OrderStatus").isin(valid_statuses)) |
        (col("o.dup_rank") > 1)
    )
    .withColumn(
        "RejectionReason",
        when(col("o.CustomerID").isNull() | (col("o.CustomerID") == ""), lit("Missing CustomerID"))
        .when(col("c.CustomerID").isNull(), lit("Unknown CustomerID"))
        .when(col("p.ProductID").isNull(), lit("Unknown ProductID"))
        .when(~col("o.OrderStatus").isin(valid_statuses), lit("Invalid OrderStatus"))
        .when(col("o.dup_rank") > 1, lit("Duplicate OrderID"))
        .otherwise(lit("Unknown rejection"))
    )
    .select(
        col("o.OrderID"),
        col("o.OrderDate"),
        col("o.CustomerID"),
        col("o.ProductID"),
        col("o.Quantity"),
        col("o.UnitPrice"),
        col("o.OrderAmount"),
        col("o.OrderStatus"),
        col("RejectionReason"),
    )
)

silver_orders = (
    joined_orders
    .where(
        (col("o.CustomerID").isNotNull()) &
        (col("o.CustomerID") != "") &
        col("o.OrderStatus").isin(valid_statuses) &
        col("c.CustomerID").isNotNull() &
        col("p.ProductID").isNotNull() &
        (col("o.dup_rank") == 1)
    )
    .select(
        col("o.OrderID"),
        col("o.OrderDate"),
        col("o.CustomerID"),
        col("o.ProductID"),
        col("o.Quantity"),
        col("o.UnitPrice"),
        col("o.OrderAmount"),
        col("o.OrderStatus"),
        col("c.Region"),
    )
)

gold_region_sales_summary = (
    silver_orders
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").alias("TotalOrderAmount"),
    )
    .orderBy("Region")
)

customers.write.mode("overwrite").format("delta").saveAsTable("silver_customers")
products.write.mode("overwrite").format("delta").saveAsTable("silver_products")
silver_orders.write.mode("overwrite").format("delta").saveAsTable("silver_orders")
silver_order_rejections.write.mode("overwrite").format("delta").saveAsTable("silver_order_rejections")
gold_region_sales_summary.write.mode("overwrite").format("delta").saveAsTable("gold_region_sales_summary")

display(
    spark.sql(
        """
        SELECT 'silver_customers' AS table_name, COUNT(*) AS row_count FROM silver_customers
        UNION ALL
        SELECT 'silver_products' AS table_name, COUNT(*) AS row_count FROM silver_products
        UNION ALL
        SELECT 'silver_orders' AS table_name, COUNT(*) AS row_count FROM silver_orders
        UNION ALL
        SELECT 'silver_order_rejections' AS table_name, COUNT(*) AS row_count FROM silver_order_rejections
        UNION ALL
        SELECT 'gold_region_sales_summary' AS table_name, COUNT(*) AS row_count FROM gold_region_sales_summary
        """
    )
)
