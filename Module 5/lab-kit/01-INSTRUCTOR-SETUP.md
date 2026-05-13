# Instructor Setup Guide

This guide prepares the Day 5 lab environment from top to bottom.

Follow these steps in order.

## 1. What You Will Build

By the end of setup, your environment should contain:

- one Fabric workspace
- one Lakehouse with uploaded raw files
- five notebooks for build, fast, slow, fail, and pass checks
- one pipeline with a visible slow step and a deliberate threshold failure
- one repaired rerun of the same pipeline
- one Warehouse with reporting tables
- one pytest automation folder with an observed-results file and tests

## 2. Before You Start

Make sure you have:

- access to Microsoft Fabric
- permission to create a workspace, Lakehouse, Warehouse, notebooks, and data pipelines
- access to the files in this `lab-kit/support-files/` folder
- access to a terminal where `python3` is available

Files you will use during setup:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/MONITORING_CHECKLIST.md`
- `support-files/scenario/AUTOMATION_BOUNDARIES.md`
- `support-files/automation/README.md`
- embedded notebook and SQL code blocks in this guide

## 3. Review the Scenario Files

Before building the environment:

1. Open `support-files/scenario/SCENARIO.md`.
2. Open `support-files/scenario/DATA_DICTIONARY.md`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Open `support-files/scenario/MONITORING_CHECKLIST.md`.
5. Open `support-files/scenario/AUTOMATION_BOUNDARIES.md`.
6. Confirm that the expected totals and runtime expectations match the teaching story you want to use.

## 4. Create the Demo Workspace

1. Sign in to Microsoft Fabric.
2. Open **Workspaces**.
3. Select **New workspace**.
4. Enter the name `ws_day5_contoso_monitoring`.
5. Add a description such as `Day 5 performance, monitoring, and automation lab workspace`.
6. Select a licensing mode that supports Fabric capacity.
7. Create the workspace.
8. Open the new workspace.

## 5. Create the Demo Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Name the Lakehouse `lh_day5_contoso_runtime`.
4. Create the Lakehouse.
5. Open the new Lakehouse.

## 6. Upload the Support Files

1. In the Lakehouse, open the **Files** area.
2. Create a folder named `day5-lab`.
3. Open the `day5-lab` folder.
4. Upload these files from `support-files/data/`:
   - `customers.csv`
   - `products.csv`
   - `orders.csv`
5. Confirm that all three files are visible after the upload completes.

## 7. Create the Notebooks

Create each notebook below, attach it to `lh_day5_contoso_runtime`, paste the matching code block, and save it.

### Notebook 1: Build performance tables

Notebook name: `nb_day5_build_perf_tables`

```python
from pyspark.sql.functions import col, count as spark_count, sum as spark_sum

# Define the Lakehouse Files path that stores the Day 5 source CSV files.
base_path = "Files/day5-lab"

# Load raw customers, products, and orders input files.
customers_df = spark.read.option("header", True).csv(f"{base_path}/customers.csv")
products_df = spark.read.option("header", True).csv(f"{base_path}/products.csv")
orders_df = spark.read.option("header", True).csv(f"{base_path}/orders.csv")

# Select and standardize customer fields for curated output.
customers_df = customers_df.select(
    col("CustomerID"),
    col("CustomerName"),
    col("Region"),
    col("CustomerSegment"),
    col("IsActive"),
)

# Select and standardize product fields; cast UnitPrice to decimal.
products_df = products_df.select(
    col("ProductID"),
    col("ProductName"),
    col("Category"),
    col("UnitPrice").cast("decimal(18,2)").alias("UnitPrice"),
    col("IsActive"),
)

# Select and standardize order fields; cast date and numeric columns.
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

# Persist curated tables to Delta for downstream pipeline activities.
customers_df.write.mode("overwrite").format("delta").saveAsTable("perf_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("perf_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("perf_orders")

# Build region-level aggregation used for performance and QA checks.
summary_df = (
    orders_df.join(customers_df, "CustomerID", "inner")
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").cast("decimal(18,2)").alias("TotalSales"),
    )
    .orderBy("Region")
)

# Save regional summary table for metric checks in later notebooks.
summary_df.write.mode("overwrite").format("delta").saveAsTable("perf_region_sales_summary")

# Display row counts to confirm all expected tables were created.
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
```

### Notebook 2: Fast metric check

Notebook name: `nb_day5_fast_metric_check`

```python
# Run a quick aggregate query for a short-duration metric checkpoint.
display(
    spark.sql(
        """
        SELECT COUNT(*) AS order_count,
               CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
        FROM perf_orders
        """
    )
)

# Emit a completion marker that appears in notebook and pipeline logs.
print("Fast metric check completed.")
```

### Notebook 3: Slow metric check

Notebook name: `nb_day5_slow_metric_check`

```python
import time

# Query regional summary output for the slower metric-check activity.
display(
    spark.sql(
        """
        SELECT Region, OrderCount, TotalSales
        FROM perf_region_sales_summary
        ORDER BY Region
        """
    )
)

# Add an intentional wait so learners can compare activity durations.
time.sleep(20)

# Emit a completion marker for the slow-check notebook.
print("Slow metric check completed after an intentional wait for duration comparison.")
```

### Notebook 4: Threshold fail

Notebook name: `nb_day5_threshold_fail`

```python
# Compute total sales metric used by the threshold gate check.
total_sales = spark.sql(
    """
    SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
    FROM perf_orders
    """
).collect()[0]["total_sales"]

# Print observed metric and intentionally fail for monitoring/rerun practice.
print(f"Observed total sales: {total_sales}")
print("Intentional Day 5 threshold failure for QA monitoring practice.")

# Raise an intentional exception to simulate threshold gate failure.
raise Exception("Intentional Day 5 threshold failure. Replace this notebook with nb_day5_threshold_pass for the rerun.")
```

### Notebook 5: Threshold pass

Notebook name: `nb_day5_threshold_pass`

```python
# Re-check key metrics after replacing the failing threshold notebook.
display(
    spark.sql(
        """
        SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales,
               COUNT(*) AS order_count
        FROM perf_orders
        """
    )
)

# Emit a success marker so pipeline logs clearly show the gate passed.
print("Threshold gate passed. The pipeline can complete successfully.")
```

## 8. Create the Demo Pipeline

1. In the workspace, select **New item**.
2. Choose **Data pipeline**.
3. Name the pipeline `pl_day5_contoso_monitoring`.
4. Open the pipeline canvas.
5. Add a **Notebook** activity named `Build performance tables`.
6. Configure it to run `nb_day5_build_perf_tables`.
7. Add a **Notebook** activity named `Fast metric check`.
8. Configure it to run `nb_day5_fast_metric_check`.
9. Add a **Notebook** activity named `Slow metric check`.
10. Configure it to run `nb_day5_slow_metric_check`.
11. Add a **Notebook** activity named `Threshold gate`.
12. Configure it to run `nb_day5_threshold_fail`.
13. Connect the activities using success paths in this order:
    - `Build performance tables` -> `Fast metric check`
    - `Fast metric check` -> `Slow metric check`
    - `Slow metric check` -> `Threshold gate`
14. Save the pipeline.

## 9. Run the Pipeline and Confirm the Failure Pattern

1. Run the pipeline.
2. Wait until the first three activities complete.
3. Confirm that the final `Threshold gate` activity fails.
4. Open the pipeline run details.
5. Confirm that:
   - the build activity succeeded
   - the fast check succeeded
   - the slow check succeeded
   - the threshold gate failed
6. Capture the activity durations from the run details.
7. Confirm that the slow step took longer than the fast step.

## 10. Review Monitoring Evidence

1. Open **Monitoring Hub** if it is available in your environment.
2. Filter to the pipeline or notebook items you just ran.
3. Capture the following:
   - activity status
   - start time
   - end time
   - duration
4. Compare the captured evidence to `MONITORING_CHECKLIST.md`.

## 11. Repair the Pipeline for the Successful Rerun

1. Return to the pipeline editor.
2. Select the `Threshold gate` activity.
3. Change the notebook from `nb_day5_threshold_fail` to `nb_day5_threshold_pass`.
4. Save the pipeline.
5. Run the pipeline again.
6. Wait until all activities complete successfully.
7. Capture the second run details and confirm that the rerun succeeded.

## 12. Create the Demo Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name the Warehouse `wh_day5_contoso_reporting`.
5. Create the Warehouse.
6. Open the new Warehouse.

## 13. Create and Load the Warehouse Tables

1. Open a new SQL query window.
2. Copy the warehouse table creation script shown below into the query editor.
3. Run the script.
4. Open a new query window.
5. Copy the warehouse data load script shown below into the query editor.
6. Run the script.

Warehouse table creation script:

```sql
-- Drop fact table first to avoid dependency issues during table reset.
IF OBJECT_ID('dbo.FactSales', 'U') IS NOT NULL
    DROP TABLE dbo.FactSales;

-- Drop product dimension if it already exists.
IF OBJECT_ID('dbo.DimProduct', 'U') IS NOT NULL
    DROP TABLE dbo.DimProduct;

-- Drop customer dimension if it already exists.
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL
    DROP TABLE dbo.DimCustomer;

-- Create customer dimension table for reporting and validation.
CREATE TABLE dbo.DimCustomer
(
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    Region VARCHAR(20) NOT NULL,
    CustomerSegment VARCHAR(30) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

-- Create product dimension table for reporting and validation.
CREATE TABLE dbo.DimProduct
(
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(30) NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

-- Create fact table that stores order-level sales transactions.
CREATE TABLE dbo.FactSales
(
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL,
    OrderAmount DECIMAL(18,2) NOT NULL,
    OrderStatus VARCHAR(20) NOT NULL
);
```

Warehouse data load script:

```sql
-- Load customer dimension seed data.
INSERT INTO dbo.DimCustomer (CustomerID, CustomerName, Region, CustomerSegment, IsActive)
VALUES
('C5001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C5002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C5003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C5004', 'City Cycle House', 'East', 'SMB', 'Y'),
('C5005', 'Adventure Works Outlet', 'North', 'SMB', 'Y'),
('C5006', 'Fabrikam Trails', 'West', 'SMB', 'Y');

-- Load product dimension seed data.
INSERT INTO dbo.DimProduct (ProductID, ProductName, Category, UnitPrice, IsActive)
VALUES
('P500', 'Trail Helmet', 'Accessories', 45.00, 'Y'),
('P501', 'Road Bike', 'Bikes', 1200.00, 'Y'),
('P502', 'Mountain Bike', 'Bikes', 1500.00, 'Y'),
('P503', 'Cycling Jersey', 'Apparel', 60.00, 'Y'),
('P504', 'Water Bottle', 'Accessories', 15.00, 'Y');

-- Load sales fact seed data used for KPI and region-level assertions.
INSERT INTO dbo.FactSales (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
VALUES
('SO50001', '2026-04-01', 'C5001', 'P501', 1, 1200.00, 1200.00, 'Complete'),
('SO50002', '2026-04-01', 'C5002', 'P503', 4, 60.00, 240.00, 'Complete'),
('SO50003', '2026-04-02', 'C5003', 'P500', 2, 45.00, 90.00, 'Complete'),
('SO50004', '2026-04-02', 'C5004', 'P502', 1, 1500.00, 1500.00, 'Complete'),
('SO50005', '2026-04-03', 'C5005', 'P504', 10, 15.00, 150.00, 'Complete'),
('SO50006', '2026-04-03', 'C5006', 'P501', 1, 1200.00, 1200.00, 'Complete'),
('SO50007', '2026-04-04', 'C5001', 'P503', 3, 60.00, 180.00, 'Complete'),
('SO50008', '2026-04-04', 'C5002', 'P504', 8, 15.00, 120.00, 'Complete'),
('SO50009', '2026-04-05', 'C5003', 'P503', 5, 60.00, 300.00, 'Complete'),
('SO50010', '2026-04-05', 'C5004', 'P500', 2, 45.00, 90.00, 'Complete');
```

## 14. Validate the Warehouse Outputs

1. Copy the validation queries shown below.
2. Run the full script in the Warehouse.
3. Compare the results to `EXPECTED_RESULTS.md`.
4. Record the observed totals and region values.

Validation queries:

```sql
-- Validate customer dimension row count.
SELECT COUNT(*) AS dimcustomer_count
FROM dbo.DimCustomer;

-- Validate product dimension row count.
SELECT COUNT(*) AS dimproduct_count
FROM dbo.DimProduct;

-- Validate fact table row count.
SELECT COUNT(*) AS factsales_count
FROM dbo.FactSales;

-- Validate total sales KPI.
SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
FROM dbo.FactSales;

-- Validate overall order count KPI.
SELECT COUNT(*) AS order_count
FROM dbo.FactSales;

-- Validate average order value KPI.
SELECT CAST(AVG(OrderAmount) AS DECIMAL(18,2)) AS average_order_value
FROM dbo.FactSales;

-- Validate region-level totals across all regions.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(f.OrderAmount) AS DECIMAL(18,2)) AS TotalSales
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c
    ON f.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;
```

## 15. Prepare the Automation Inputs

1. Open the folder `support-files/automation/`.
2. Read `README.md`.
3. Copy `observed_results.template.json` to a new file named `observed_results.json`.
4. Replace the placeholder values in `observed_results.json` with the values you captured from Fabric.
5. Use `sample_observed_results.json` as a reference for value format and status casing.

Example populated `observed_results.json` (sample values):

```json
{
  "pipeline": {
    "run_1_status": "Failed",
    "run_2_status": "Succeeded",
    "fast_activity_status": "Succeeded",
    "slow_activity_status": "Succeeded",
    "threshold_activity_initial_status": "Failed",
    "threshold_activity_rerun_status": "Succeeded",
    "fast_duration_seconds": 8,
    "slow_duration_seconds": 28,
    "slow_activity_longer_than_fast": true
  },
  "warehouse": {
    "factsales_count": 10,
    "total_sales": 5070.0,
    "order_count": 10,
    "average_order_value": 507.0,
    "region_totals": {
      "East": { "order_count": 2, "total_sales": 1590.0 },
      "North": { "order_count": 3, "total_sales": 1530.0 },
      "South": { "order_count": 2, "total_sales": 390.0 },
      "West": { "order_count": 3, "total_sales": 1560.0 }
    }
  }
}
```

## 16. Run the Pytest Suite

1. Open a terminal in `support-files/automation/`.
2. If `pytest` is not installed, run:

```bash
# Install required Python dependencies for local validation tests.
python3 -m pip install -r requirements.txt
```

3. Run the test suite:

```bash
# Run the automated Day 5 result validation test suite.
python3 -m pytest tests/test_day5_results.py
```

4. Confirm that all tests pass when the observed results match expectations.

## 17. Final Instructor Validation Checklist

Before learners begin, confirm that:

- the workspace `ws_day5_contoso_monitoring` exists
- the Lakehouse `lh_day5_contoso_runtime` exists
- the uploaded files are visible in `Files/day5-lab`
- the five notebooks exist and are attached to the Lakehouse
- the pipeline exists
- one failed pipeline run is visible
- one successful rerun is visible
- the slow activity duration is greater than the fast activity duration
- the Warehouse exists and is loaded
- the validation queries match `EXPECTED_RESULTS.md`
- the pytest suite passes with a populated observed-results file

## 18. Files to Share with Learners

Share or point learners to these files:

- `02-LEARNER-LAB-GUIDE.md`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/MONITORING_CHECKLIST.md`
- `support-files/scenario/AUTOMATION_BOUNDARIES.md`
- `support-files/automation/README.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`

## 19. Troubleshooting Notes

- If the pipeline run finishes too quickly to compare durations, rerun the slow notebook directly and then rerun the pipeline.
- If the first pipeline run does not fail, make sure the threshold activity still points to `nb_day5_threshold_fail`.
- If the rerun still fails, confirm that the threshold activity was switched to `nb_day5_threshold_pass`.
- If `pytest` fails immediately because the observed-results file is missing, confirm that `observed_results.json` exists in the automation folder.
- If the Warehouse totals do not match expectations, rerun the create and load scripts in order.
