# Instructor Setup Guide

This guide prepares the Day 2 lab environment from top to bottom.

Follow these steps in order.

## 1. What You Will Build

By the end of setup, your environment should contain:

- one Fabric workspace
- one Lakehouse
- raw support files uploaded into the Lakehouse
- Bronze tables created from the raw files
- Silver and Gold tables created through notebook transformations
- an incremental load file used to test late-arriving and invalid data handling

## 2. Before You Start

Make sure you have:

- access to Microsoft Fabric
- permission to create a workspace, Lakehouse, and notebooks
- access to the files in this `lab-kit/support-files/` folder

Files you will use during setup:

- `support-files/data/customers_raw.csv`
- `support-files/data/products_raw.csv`
- `support-files/data/orders_full_raw.csv`
- `support-files/data/orders_incremental_raw.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/KNOWN_ISSUES.md`
- embedded notebook and SQL code blocks in this guide

## 3. Review the Scenario Files

Before building the environment:

1. Open `support-files/scenario/SCENARIO.md`.
2. Open `support-files/scenario/DATA_DICTIONARY.md`.
3. Open `support-files/scenario/KNOWN_ISSUES.md`.
4. Open `support-files/scenario/EXPECTED_RESULTS.md`.
5. Confirm that the raw issues and expected results match the story you want to teach.

## 4. Create the Demo Workspace

1. Sign in to Microsoft Fabric.
2. Open **Workspaces**.
3. Select **New workspace**.
4. Enter the name `ws_day2_contoso_quality`.
5. Add a description such as `Day 2 Data Validation & Quality Testing lab workspace`.
6. Select a licensing mode that supports Fabric capacity.
7. Create the workspace.
8. Open the new workspace.

## 5. Create the Demo Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Name the Lakehouse `lh_day2_contoso_quality`.
4. Create the Lakehouse.
5. Open the new Lakehouse.

## 6. Upload the Raw Support Files

1. In the Lakehouse, open the **Files** area.
2. Create a folder named `day2-lab`.
3. Open the `day2-lab` folder.
4. Upload these files from `support-files/data/`:
   - `customers_raw.csv`
   - `products_raw.csv`
   - `orders_full_raw.csv`
   - `orders_incremental_raw.csv`
5. Confirm that all four files are visible in the folder after the upload completes.

## 7. Create the Bronze Notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_bronze_load`.
5. Open the notebook.
6. Attach the notebook to `lh_day2_contoso_quality`.
7. Copy the Bronze notebook code block shown below.
8. Paste the contents into the first notebook cell.
9. Run the notebook.
10. Wait until it completes successfully.
11. Return to the Lakehouse and confirm that the Bronze tables exist:
    - `bronze_customers`
    - `bronze_products`
    - `bronze_orders`

Bronze notebook code:

```python
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
```

## 8. Create the Silver and Gold Notebook

1. Return to the workspace.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_silver_gold_build`.
5. Open the notebook.
6. Attach the notebook to `lh_day2_contoso_quality`.
7. Copy the Silver/Gold notebook code block shown below.
8. Paste the contents into the first notebook cell.
9. Run the notebook.
10. Wait until it completes successfully.
11. Return to the Lakehouse and confirm that the following tables now exist:
    - `silver_customers`
    - `silver_products`
    - `silver_orders`
    - `silver_order_rejections`
    - `gold_region_sales_summary`

Silver/Gold notebook code:

```python
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
```

## 9. Validate the Full-Load State

1. Open the Lakehouse SQL analytics endpoint if available.
2. Copy the `FULL LOAD VALIDATION` queries shown below.
3. Paste them into the SQL analytics endpoint query window.
4. Run the queries.
5. Compare the results to `support-files/scenario/EXPECTED_RESULTS.md`.
6. Confirm that the results match the expected Bronze, Silver, rejection, and Gold values.

Full-load validation queries:

```sql
SELECT COUNT(*) AS bronze_customers_count
FROM bronze_customers;

SELECT COUNT(*) AS bronze_products_count
FROM bronze_products;

SELECT COUNT(*) AS bronze_orders_count
FROM bronze_orders;

SELECT COUNT(*) AS silver_customers_count
FROM silver_customers;

SELECT COUNT(*) AS silver_products_count
FROM silver_products;

SELECT COUNT(*) AS silver_orders_count
FROM silver_orders;

SELECT COUNT(*) AS silver_order_rejections_count
FROM silver_order_rejections;

SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;

SELECT RejectionReason, COUNT(*) AS rejection_count
FROM silver_order_rejections
GROUP BY RejectionReason
ORDER BY RejectionReason;
```

## 10. Create the Incremental Notebook

1. Return to the workspace.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_incremental_load`.
5. Open the notebook.
6. Attach the notebook to `lh_day2_contoso_quality`.
7. Copy the incremental notebook code block shown below.
8. Paste the contents into the first notebook cell.
9. Run the notebook.
10. Wait until it completes successfully.

Incremental notebook code:

```python
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
```

## 11. Validate the Incremental State

1. Open the Lakehouse SQL analytics endpoint again.
2. Copy the `INCREMENTAL LOAD VALIDATION` queries shown below.
3. Paste the queries into the SQL query editor.
4. Run the queries.
5. Compare the results with `EXPECTED_RESULTS.md`.
6. Confirm that the accepted and rejected incremental rows match expectations.

Incremental validation queries:

```sql
SELECT COUNT(*) AS silver_orders_count_after_incremental
FROM silver_orders;

SELECT COUNT(*) AS silver_rejections_count_after_incremental
FROM silver_order_rejections;

SELECT COUNT(*) AS accepted_late_arriving_count
FROM silver_orders
WHERE OrderID = 'SO20008';

SELECT COUNT(*) AS duplicate_replay_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20004';

SELECT COUNT(*) AS invalid_status_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20009';

SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;
```

## 12. Final Instructor Validation Checklist

Before the learners begin, confirm that:

- the workspace `ws_day2_contoso_quality` exists
- the Lakehouse `lh_day2_contoso_quality` exists
- the raw files are visible in `Files/day2-lab`
- the Bronze tables exist
- the Silver tables exist
- the Gold summary table exists
- the rejection table exists
- the incremental notebook has been run successfully at least once
- the validation queries match the expected results document

## 13. Files to Share with Learners

Share or point learners to these files:

- `02-LEARNER-LAB-GUIDE.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/KNOWN_ISSUES.md`

## 14. Troubleshooting Notes

- If a table is not visible after a notebook run, refresh the Lakehouse explorer.
- If the SQL endpoint is not available to learners, the lab can still be completed by inspecting notebook output and table previews.
- If a notebook fails because a table already exists, rerun the Bronze notebook first and then rerun the Silver/Gold notebook.
- If incremental results are not as expected, rerun the Bronze notebook, then the Silver/Gold notebook, then the incremental notebook in that order.
