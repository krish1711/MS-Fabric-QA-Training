# Day 2 incremental notebook
# Attach this notebook to the Lakehouse `lh_day2_contoso_quality`
# before running the code.

from pyspark.sql.functions import col, lit, to_date, trim, when

valid_statuses = ["Shipped", "Processing", "Cancelled"]

silver_customers = spark.table("silver_customers").select("CustomerID", "Region")
silver_products = spark.table("silver_products").select("ProductID")
silver_orders = spark.table("silver_orders")
silver_rejections = spark.table("silver_order_rejections")

incremental_orders = (
    spark.read.option("header", True).csv("Files/day2-lab/orders_incremental_raw.csv")
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

existing_order_ids = silver_orders.select("OrderID").withColumn("already_loaded", lit(True))

joined_incremental = (
    incremental_orders.alias("i")
    .join(silver_customers.alias("c"), col("i.CustomerID") == col("c.CustomerID"), "left")
    .join(silver_products.alias("p"), col("i.ProductID") == col("p.ProductID"), "left")
    .join(existing_order_ids.alias("e"), col("i.OrderID") == col("e.OrderID"), "left")
)

accepted_incremental = (
    joined_incremental
    .where(
        col("c.CustomerID").isNotNull() &
        col("p.ProductID").isNotNull() &
        col("e.already_loaded").isNull() &
        col("i.OrderStatus").isin(valid_statuses)
    )
    .select(
        col("i.OrderID"),
        col("i.OrderDate"),
        col("i.CustomerID"),
        col("i.ProductID"),
        col("i.Quantity"),
        col("i.UnitPrice"),
        col("i.OrderAmount"),
        col("i.OrderStatus"),
        col("c.Region"),
    )
)

rejected_incremental = (
    joined_incremental
    .where(
        col("c.CustomerID").isNull() |
        col("p.ProductID").isNull() |
        col("e.already_loaded").isNotNull() |
        (~col("i.OrderStatus").isin(valid_statuses))
    )
    .withColumn(
        "RejectionReason",
        when(col("c.CustomerID").isNull(), lit("Unknown CustomerID"))
        .when(col("p.ProductID").isNull(), lit("Unknown ProductID"))
        .when(col("e.already_loaded").isNotNull(), lit("Duplicate replay"))
        .when(~col("i.OrderStatus").isin(valid_statuses), lit("Invalid OrderStatus"))
        .otherwise(lit("Unknown rejection"))
    )
    .select(
        col("i.OrderID"),
        col("i.OrderDate"),
        col("i.CustomerID"),
        col("i.ProductID"),
        col("i.Quantity"),
        col("i.UnitPrice"),
        col("i.OrderAmount"),
        col("i.OrderStatus"),
        col("RejectionReason"),
    )
)

updated_silver_orders = silver_orders.unionByName(accepted_incremental)
updated_rejections = silver_rejections.unionByName(rejected_incremental)

updated_gold = (
    updated_silver_orders
    .groupBy("Region")
    .sum("OrderAmount")
    .withColumnRenamed("sum(OrderAmount)", "TotalOrderAmount")
)

order_counts = (
    updated_silver_orders
    .groupBy("Region")
    .count()
    .withColumnRenamed("count", "OrderCount")
)

updated_gold = (
    updated_gold
    .join(order_counts, ["Region"])
    .select("Region", "OrderCount", "TotalOrderAmount")
    .orderBy("Region")
)

updated_silver_orders.write.mode("overwrite").format("delta").saveAsTable("silver_orders")
updated_rejections.write.mode("overwrite").format("delta").saveAsTable("silver_order_rejections")
updated_gold.write.mode("overwrite").format("delta").saveAsTable("gold_region_sales_summary")

display(
    spark.sql(
        """
        SELECT 'accepted_incremental_rows' AS metric, COUNT(*) AS value FROM silver_orders WHERE OrderID = 'SO20008'
        UNION ALL
        SELECT 'rejected_incremental_rows' AS metric, COUNT(*) AS value FROM silver_order_rejections WHERE OrderID IN ('SO20004', 'SO20009')
        """
    )
)
