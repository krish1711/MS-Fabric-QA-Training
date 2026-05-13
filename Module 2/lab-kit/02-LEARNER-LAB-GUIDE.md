# Day 2 Lab: Data Validation & Quality Testing

This lab is designed as a true end-to-end hands-on exercise. You will build a small medallion-style Fabric quality-testing environment, inspect raw defects, validate transformed outputs, and record QA evidence from top to bottom.

## Lab scenario

You are part of a QA team validating the data quality flow for **Contoso Outdoor Retail** in Microsoft Fabric.

The raw data includes intentional issues so that you can practice:

- schema and completeness checks
- duplicate and validity checks
- business-rule validation
- full-load vs. incremental-load testing
- late-arriving and invalid record analysis

## Lab objectives

By the end of this lab, you should be able to:

- create a Day 2 Fabric workspace and Lakehouse
- load raw files into Bronze tables
- inspect and explain quality issues in Bronze data
- build Silver and Gold outputs
- validate row counts, rejections, and summaries
- apply an incremental file and observe accepted vs. rejected records
- record QA findings and quality-focused test cases

## Estimated time

60 to 75 minutes

## Prerequisites

Before you begin, make sure that:

- you can sign in to Microsoft Fabric
- you have permission to create items in a Fabric workspace
- you have access to the files in `lab-kit/support-files/`

## Files you will use

Keep these files available during the lab:

- `support-files/data/customers_raw.csv`
- `support-files/data/products_raw.csv`
- `support-files/data/orders_full_raw.csv`
- `support-files/data/orders_incremental_raw.csv`
- `support-files/scenario/KNOWN_ISSUES.md`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- embedded notebook and SQL code blocks in this guide

## Recommended item names

Use these names during the lab:

- Workspace: `ws_day2_contoso_quality`
- Lakehouse: `lh_day2_contoso_quality`
- Notebook 1: `nb_day2_bronze_load`
- Notebook 2: `nb_day2_silver_gold_build`
- Notebook 3: `nb_day2_incremental_load`

## Before you start

1. Open `support-files/templates/learner-worksheet.md`.
2. Open `support-files/templates/evidence-log-template.csv`.
3. Open `support-files/scenario/KNOWN_ISSUES.md`.
4. Open `support-files/scenario/EXPECTED_RESULTS.md`.
5. Keep those files available in a separate window or tab while you work.

## Exercise 1: Create the workspace and Lakehouse

In this exercise, you will create the Fabric workspace and Lakehouse that will hold the Day 2 demo data.

### Task 1: Create the workspace

1. Open Microsoft Fabric in your browser.
2. Sign in with your Fabric account - https://app.fabric.microsoft.com/ 
3. In the left navigation menu, select **Workspaces**.
4. Select **New workspace**.
5. Enter the workspace name `ws_day2_contoso_quality`.
6. In the description field, enter `Day 2 Data Validation & Quality Testing lab workspace`.
7. Select a licensing mode that supports Fabric capacity in your environment.
8. Create the workspace.
9. When the workspace opens, verify that it is empty.
10. In your learner worksheet, record the workspace name.

### Task 2: Create the Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Enter the name `lh_day2_contoso_quality`.
4. Create the Lakehouse.
5. Wait until the Lakehouse opens.
6. Confirm that you can see the **Lakehouse explorer** with **Tables** and **Files**.
7. In your worksheet, record the Lakehouse name.

## Exercise 2: Upload the raw support files

In this exercise, you will upload the local CSV support files into the Lakehouse.

### Task 1: Create the upload folder

1. In the Lakehouse, open the **Files** area.
2. Open the menu for **Files**.
3. Select the option to create a new folder or subfolder.
4. Create a folder named `day2-lab`.
5. Open the `day2-lab` folder.

### Task 2: Upload the CSV files

1. In the `day2-lab` folder, select the upload option.
2. Choose **Upload files**.
3. Browse to the local folder `support-files/data/`.
4. Select these four files:
   - `customers_raw.csv`
   - `products_raw.csv`
   - `orders_full_raw.csv`
   - `orders_incremental_raw.csv`
5. Upload the files.
6. Wait until the upload completes.
7. Confirm that all four files are visible in the `day2-lab` folder.
8. Open each file preview if your environment allows it.
9. In your worksheet, record the names of the uploaded files.
10. In the evidence log, add one row noting that the raw support files are visible in the Lakehouse.

## Exercise 3: Build the Bronze tables

In this exercise, you will create Bronze tables from the raw support files.

### Task 1: Create the Bronze notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_bronze_load`.
5. Open the notebook.

### Task 2: Attach the Bronze notebook to the Lakehouse

1. In the notebook, find the Lakehouse attachment selector.
2. Attach the notebook to `lh_day2_contoso_quality`.
3. Confirm that the notebook is associated with the correct Lakehouse.

### Task 3: Paste and run the Bronze notebook code

1. Copy the Bronze notebook code block shown below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait for the notebook to complete successfully.
5. Review the output, which should show Bronze row counts.

Bronze notebook code:

```python
from pyspark.sql.functions import col

# Base Lakehouse files folder used in this lab.
base_path = "Files/day2-lab"

# Read each raw CSV file from Lakehouse Files into a DataFrame.
customers_df = spark.read.option("header", True).csv(f"{base_path}/customers_raw.csv")
products_df = spark.read.option("header", True).csv(f"{base_path}/products_raw.csv")
orders_df = spark.read.option("header", True).csv(f"{base_path}/orders_full_raw.csv")

# Save raw data as Bronze Delta tables (overwrite allows safe reruns).
customers_df.write.mode("overwrite").format("delta").saveAsTable("bronze_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("bronze_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("bronze_orders")

# Display Bronze row counts so we can validate the load completed.
display(
    spark.sql(
        """
        -- Count rows loaded into Bronze customers.
        SELECT 'bronze_customers' AS table_name, COUNT(*) AS row_count FROM bronze_customers
        UNION ALL
        -- Count rows loaded into Bronze products.
        SELECT 'bronze_products' AS table_name, COUNT(*) AS row_count FROM bronze_products
        UNION ALL
        -- Count rows loaded into Bronze orders.
        SELECT 'bronze_orders' AS table_name, COUNT(*) AS row_count FROM bronze_orders
        """
    )
)
```

### Task 4: Verify the Bronze tables

1. Return to the Lakehouse `lh_day2_contoso_quality`.
2. Open the **Tables** area.
3. Refresh the Lakehouse explorer if necessary.
4. Confirm that these tables exist:
   - `bronze_customers`
   - `bronze_products`
   - `bronze_orders`
5. Open each table and inspect a few rows.
6. In your worksheet, write one sentence describing what Bronze data represents in QA terms.
7. In the evidence log, add one row noting that the Bronze tables are visible.

## Exercise 4: Inspect the known quality issues in Bronze

In this exercise, you will compare the raw data to the known issue summary.

### Task 1: Review the issue summary

1. Open `support-files/scenario/KNOWN_ISSUES.md`.
2. Read the list of known data issues in the raw data.
3. Note the categories of issues described in the file.

### Task 2: Compare Bronze data to the issue list

1. Open `bronze_orders`.
2. Inspect sample rows and look for issue patterns mentioned in `KNOWN_ISSUES.md`.
3. Open `bronze_customers`.
4. Inspect sample rows and look for issue patterns mentioned in `KNOWN_ISSUES.md`.
5. Open `bronze_products`.
6. Inspect sample rows and look for issue patterns mentioned in `KNOWN_ISSUES.md`.
7. In your worksheet, write down at least three observed Bronze issues.
8. In the evidence log, add one row describing what defects are visible in Bronze.

## Exercise 5: Build the Silver and Gold tables

In this exercise, you will create Silver and Gold tables that apply cleansing and business logic.

Before you run this exercise, confirm that `bronze_customers`, `bronze_products`, and `bronze_orders` already exist in the Lakehouse **Tables** area. If any are missing, rerun Exercise 3 first.

### Task 1: Create the Silver/Gold notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_silver_gold_build`.
5. Open the notebook.

### Task 2: Attach the notebook to the Lakehouse

1. Attach the notebook to `lh_day2_contoso_quality`.
2. Confirm that the correct Lakehouse is attached.

### Task 3: Paste and run the Silver/Gold notebook code

1. Copy the Silver/Gold notebook code block shown below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait for the notebook to finish successfully.
5. Review the output and note the counts for accepted and rejected rows.

Silver/Gold notebook code:

```python
from pyspark.sql.functions import col, lit, to_date, trim, row_number, sum as spark_sum, count as spark_count, when
from pyspark.sql.window import Window

# Build Silver customers by trimming fields and dropping rows with missing Region.
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

# Build Silver products by trimming fields and dropping rows with missing Category.
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

# Standardize Bronze orders: trim strings, parse date, cast numeric columns.
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

# Allowed business statuses for accepted orders.
valid_statuses = ["Shipped", "Processing", "Cancelled"]

# Rank duplicates by OrderID so the earliest record is retained.
order_window = Window.partitionBy("OrderID").orderBy(col("OrderDate").asc())
orders_with_rank = raw_orders.withColumn("dup_rank", row_number().over(order_window))

# Join orders with validated customer and product dimensions.
joined_orders = (
    orders_with_rank.alias("o")
    .join(customers.select("CustomerID", "Region").alias("c"), col("o.CustomerID") == col("c.CustomerID"), "left")
    .join(products.select("ProductID").alias("p"), col("o.ProductID") == col("p.ProductID"), "left")
)

# Route invalid records to the Silver rejection table with rejection reasons.
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

# Keep only valid records as Silver orders, including customer Region.
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

# Build Gold summary: order count and total amount by Region.
gold_region_sales_summary = (
    silver_orders
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").alias("TotalOrderAmount"),
    )
    .orderBy("Region")
)

# Persist transformed outputs as Silver and Gold Delta tables.
customers.write.mode("overwrite").format("delta").saveAsTable("silver_customers")
products.write.mode("overwrite").format("delta").saveAsTable("silver_products")
silver_orders.write.mode("overwrite").format("delta").saveAsTable("silver_orders")
silver_order_rejections.write.mode("overwrite").format("delta").saveAsTable("silver_order_rejections")
gold_region_sales_summary.write.mode("overwrite").format("delta").saveAsTable("gold_region_sales_summary")

# Display Silver/Gold row counts for quick validation.
display(
    spark.sql(
        """
        -- Silver customers row count.
        SELECT 'silver_customers' AS table_name, COUNT(*) AS row_count FROM silver_customers
        UNION ALL
        -- Silver products row count.
        SELECT 'silver_products' AS table_name, COUNT(*) AS row_count FROM silver_products
        UNION ALL
        -- Silver accepted orders row count.
        SELECT 'silver_orders' AS table_name, COUNT(*) AS row_count FROM silver_orders
        UNION ALL
        -- Silver rejected orders row count.
        SELECT 'silver_order_rejections' AS table_name, COUNT(*) AS row_count FROM silver_order_rejections
        UNION ALL
        -- Gold summary row count.
        SELECT 'gold_region_sales_summary' AS table_name, COUNT(*) AS row_count FROM gold_region_sales_summary
        """
    )
)
```

### Task 4: Verify the Silver and Gold tables

1. Return to the Lakehouse.
2. Refresh the **Tables** area.
3. Confirm that the following tables exist:
   - `silver_customers`
   - `silver_products`
   - `silver_orders`
   - `silver_order_rejections`
   - `gold_region_sales_summary`
4. Open the rejection table and inspect a few rows.
5. Open the Gold summary table and inspect the aggregated results.
6. In your worksheet, write one sentence describing what Silver data represents in QA terms.
7. In your worksheet, write one sentence describing what Gold data represents in QA terms.

## Exercise 6: Run the full-load validation checks

In this exercise, you will validate the full-load state using SQL queries.

### Task 1: Open the Lakehouse SQL analytics endpoint

1. In the Lakehouse page, switch from the **Lakehouse** view to the **SQL analytics endpoint** if available.
2. Wait until the SQL interface opens.
3. Open a new SQL query window.

### Task 2: Run the full-load validation queries

1. Copy the `FULL LOAD VALIDATION` queries shown below.
2. Paste the queries into the SQL query editor.
3. Run the queries.
4. If you receive a table-not-found error in the SQL endpoint, wait 1 to 2 minutes, refresh the SQL endpoint, and run the queries again.
5. Review the results carefully.

Full-load validation queries:

```sql
-- Bronze customers row count (raw loaded records).
SELECT COUNT(*) AS bronze_customers_count
FROM bronze_customers;

-- Bronze products row count (raw loaded records).
SELECT COUNT(*) AS bronze_products_count
FROM bronze_products;

-- Bronze orders row count (raw loaded records).
SELECT COUNT(*) AS bronze_orders_count
FROM bronze_orders;

-- Silver customers row count (after cleansing).
SELECT COUNT(*) AS silver_customers_count
FROM silver_customers;

-- Silver products row count (after cleansing).
SELECT COUNT(*) AS silver_products_count
FROM silver_products;

-- Silver accepted orders row count.
SELECT COUNT(*) AS silver_orders_count
FROM silver_orders;

-- Silver rejected orders row count.
SELECT COUNT(*) AS silver_order_rejections_count
FROM silver_order_rejections;

-- Gold business summary by Region.
SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;

-- Rejection distribution by reason for QA validation.
SELECT RejectionReason, COUNT(*) AS rejection_count
FROM silver_order_rejections
GROUP BY RejectionReason
ORDER BY RejectionReason;
```

### Task 3: Compare the results with expected values

1. Open `support-files/scenario/EXPECTED_RESULTS.md`.
2. Compare your query results to the expected values for:
   - Bronze row counts
   - Silver row counts
   - rejection counts
   - Gold region summary
3. Record the results in your worksheet.
4. In the evidence log, add one row describing the validation query output.

If your environment does not expose the Lakehouse SQL analytics endpoint, continue the lab by using notebook outputs and table previews as evidence.

## Exercise 7: Create and test the incremental-load scenario

In this exercise, you will apply the incremental input file and inspect accepted versus rejected outcomes.

This incremental notebook is designed to be rerun-safe: it keeps one accepted row per `OrderID` and one rejection per `OrderID` + `RejectionReason`, so repeated runs do not keep inflating counts.

### Task 1: Create the incremental notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day2_incremental_load`.
5. Open the notebook.

### Task 2: Attach the notebook to the Lakehouse

1. Attach the notebook to `lh_day2_contoso_quality`.
2. Confirm that the correct Lakehouse is attached.

### Task 3: Paste and run the incremental notebook code

1. Copy the incremental notebook code block shown below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait for the notebook to finish successfully.
5. Review the output and note how many incremental rows were accepted and rejected.

Incremental notebook code:

```python
from pyspark.sql.functions import col, lit, to_date, trim, when

# Allowed business statuses for incremental acceptance.
valid_statuses = ["Shipped", "Processing", "Cancelled"]

# Load current Silver tables as the baseline state.
silver_customers = spark.table("silver_customers").select("CustomerID", "Region")
silver_products = spark.table("silver_products").select("ProductID")
silver_orders = spark.table("silver_orders")
silver_rejections = spark.table("silver_order_rejections")

# Load and standardize incremental raw orders file.
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

# Use full-load order IDs as baseline replay keys (stable across reruns).
baseline_order_ids = (
    spark.table("bronze_orders")
    .select(trim(col("OrderID")).alias("OrderID"))
    .dropDuplicates()
)

# Flag baseline order IDs so replay rows can be rejected.
existing_order_ids = baseline_order_ids.withColumn("already_loaded", lit(True))

# Join incremental rows to customer/product dimensions and replay baseline.
joined_incremental = (
    incremental_orders.alias("i")
    .join(silver_customers.alias("c"), col("i.CustomerID") == col("c.CustomerID"), "left")
    .join(silver_products.alias("p"), col("i.ProductID") == col("p.ProductID"), "left")
    .join(existing_order_ids.alias("e"), col("i.OrderID") == col("e.OrderID"), "left")
)

# Keep only valid, new incremental rows.
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

# Route invalid or replay incremental rows to rejections with reasons.
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

# Merge accepted rows into Silver orders and keep one row per OrderID.
updated_silver_orders = (
    silver_orders
    .unionByName(accepted_incremental)
    .dropDuplicates(["OrderID"])
)

# Merge rejected rows and keep one row per OrderID + reason.
updated_rejections = (
    silver_rejections
    .unionByName(rejected_incremental)
    .dropDuplicates(["OrderID", "RejectionReason"])
)

# Recompute Gold totals from the updated Silver orders.
updated_gold = (
    updated_silver_orders
    .groupBy("Region")
    .sum("OrderAmount")
    .withColumnRenamed("sum(OrderAmount)", "TotalOrderAmount")
)

# Compute order counts by Region for Gold.
order_counts = (
    updated_silver_orders
    .groupBy("Region")
    .count()
    .withColumnRenamed("count", "OrderCount")
)

# Combine totals + counts into the final Gold summary shape.
updated_gold = (
    updated_gold
    .join(order_counts, ["Region"])
    .select("Region", "OrderCount", "TotalOrderAmount")
    .orderBy("Region")
)

# Persist updated Silver and Gold tables.
updated_silver_orders.write.mode("overwrite").format("delta").saveAsTable("silver_orders")
updated_rejections.write.mode("overwrite").format("delta").saveAsTable("silver_order_rejections")
updated_gold.write.mode("overwrite").format("delta").saveAsTable("gold_region_sales_summary")

# Show quick acceptance/rejection checks for known incremental rows.
display(
    spark.sql(
        """
        -- Late-arriving valid row should be accepted once.
        SELECT 'accepted_incremental_rows' AS metric, COUNT(*) AS value FROM silver_orders WHERE OrderID = 'SO20008'
        UNION ALL
        -- Known duplicate and invalid-status rows should be present in rejections.
        SELECT 'rejected_incremental_rows' AS metric, COUNT(*) AS value FROM silver_order_rejections WHERE OrderID IN ('SO20004', 'SO20009')
        """
    )
)
```

## Exercise 8: Validate the incremental-load results

In this exercise, you will verify the updated state after the incremental file is applied.

### Task 1: Run the incremental validation queries

1. Open the SQL analytics endpoint again if available.
2. Copy the `INCREMENTAL LOAD VALIDATION` queries shown below.
3. Paste the queries into the SQL query editor.
4. Run the queries.
5. Review the results.

Incremental validation queries:

```sql
-- Total accepted Silver orders after incremental processing.
SELECT COUNT(*) AS silver_orders_count_after_incremental
FROM silver_orders;

-- Total rejected Silver rows after incremental processing.
SELECT COUNT(*) AS silver_rejections_count_after_incremental
FROM silver_order_rejections;

-- Verify the late-arriving valid order was accepted.
SELECT COUNT(*) AS accepted_late_arriving_count
FROM silver_orders
WHERE OrderID = 'SO20008';

-- Verify duplicate replay row was rejected.
SELECT COUNT(*) AS duplicate_replay_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20004';

-- Verify invalid status row was rejected.
SELECT COUNT(*) AS invalid_status_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20009';

-- Validate Gold aggregates after incremental updates.
SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;
```

### Task 2: Compare the results to expected values

1. Open `EXPECTED_RESULTS.md`.
2. Compare your incremental validation results to the expected values.
3. Confirm that:
   - accepted incremental rows behave as expected
   - rejected incremental rows appear in the rejection output
   - the Gold summary reflects only accepted rows
4. Record the results in your worksheet.
5. In the evidence log, add one row describing the incremental validation results.

## Exercise 9: Perform the Day 2 QA review

In this exercise, you will behave like a QA analyst and summarize what happened in the data quality flow.

### Task 1: Compare Bronze, Silver, and Gold

In your worksheet, answer the following:

1. What kinds of issues are visible in Bronze?
2. What changes between Bronze and Silver?
3. What does Gold represent that Bronze does not?
4. Which layer is best for:
   - raw issue visibility
   - cleansing validation
   - business-ready reconciliation

Then write one comparison statement summarizing the role of Bronze, Silver, and Gold in QA terms.

### Task 2: Record data quality test ideas

Based on this lab, write at least five test ideas in your worksheet. Include examples such as:

- schema validation
- null checks
- duplicate checks
- invalid reference checks
- invalid business status checks
- incremental replay checks
- late-arriving record checks

### Task 3: Record evidence sources

List at least five places where QA evidence was collected during the lab.

Examples include:

- raw file previews
- Bronze table previews
- SQL query output
- notebook output
- rejection table contents
- Gold summary table

Record these in your worksheet.

## Exercise 10: Complete the lab deliverables

Before you finish, verify that your learner worksheet includes:

- workspace name
- Lakehouse name
- uploaded file names
- Bronze, Silver, and Gold observations
- known issue observations
- full-load validation results
- incremental-load validation results
- one medallion comparison statement
- at least five test ideas
- at least five QA evidence sources

Also verify that your evidence log has at least five completed entries.

## What you should conclude

By the end of this lab, you should be able to say:

- raw data quality issues should be expected and observed in Bronze
- Silver is where quality rules and rejection behavior become visible
- Gold should only reflect trusted, business-ready outputs
- incremental loads require separate QA thinking from full loads
- good data validation produces evidence, not just assumptions

## Clean up resources

If this was a personal practice environment and you no longer need it:

1. Return to the workspace.
2. Open **Workspace settings**.
3. Locate the workspace removal option.
4. Remove the workspace.

Do not remove the workspace if it is a shared instructor-led environment.

## Troubleshooting

- If the uploaded files do not appear, refresh the Lakehouse file explorer.
- If Bronze tables do not appear after the notebook run, refresh the **Tables** area.
- If Silver or Gold tables do not appear, rerun the Silver/Gold notebook.
- If incremental results do not match expectations, rerun the Bronze notebook, then the Silver/Gold notebook, then the incremental notebook in that order.
- If query results do not match `EXPECTED_RESULTS.md`, record the mismatch as a QA finding.
- If the SQL endpoint is unavailable in your environment, use notebook outputs and table previews as evidence and continue.
