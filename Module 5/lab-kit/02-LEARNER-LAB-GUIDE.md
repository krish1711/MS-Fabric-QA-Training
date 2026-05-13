# Module 5 Lab: Performance, Monitoring & Test Automation Fundamentals

This lab is designed as a true end-to-end hands-on exercise. You will upload raw files, build a Fabric pipeline with fast, slow, and threshold-check activities, compare run durations, review monitoring evidence, validate Warehouse outputs, and run a small pytest suite against observed results.

## Lab scenario

You are part of a QA team preparing a Microsoft Fabric solution for release at **Contoso Outdoor Retail**.

The solution already produces the correct data, but the team now needs release-readiness evidence. Your job is to prove that:

- the pipeline behaves consistently across runs
- slower steps can be identified from run history
- failure patterns are visible and understandable
- reporting totals still match the truth set
- stable observed results can be validated automatically with pytest

## Lab objectives

By the end of this lab, you should be able to:

- compare fast and slow pipeline activity durations
- inspect failure patterns in Fabric run history
- capture release-readiness evidence from monitoring surfaces
- validate reporting outputs with SQL
- populate an observed-results file and run pytest
- explain which checks are stable automation candidates

## Estimated time

75 to 90 minutes

## Prerequisites

Before you begin, make sure that:

- you can sign in to Microsoft Fabric
- you have permission to create items in a Fabric workspace
- you have access to the files in `lab-kit/support-files/`
- you can run `python3` in a local terminal

## Files you will use

Keep these files available during the lab:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/MONITORING_CHECKLIST.md`
- `support-files/scenario/AUTOMATION_BOUNDARIES.md`
- `support-files/automation/README.md`
- `support-files/automation/observed_results.template.json`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- embedded notebook and SQL code blocks in this guide

## Recommended item names

Use these names during the lab:

- Workspace: `ws_day5_contoso_monitoring`
- Lakehouse: `lh_day5_contoso_runtime`
- Warehouse: `wh_day5_contoso_reporting`
- Notebook 1: `nb_day5_build_perf_tables`
- Notebook 2: `nb_day5_fast_metric_check`
- Notebook 3: `nb_day5_slow_metric_check`
- Notebook 4: `nb_day5_threshold_fail`
- Notebook 5: `nb_day5_threshold_pass`
- Pipeline: `pl_day5_contoso_monitoring`

## Before you start

1. Open `support-files/templates/learner-worksheet.md`.
2. Open `support-files/templates/evidence-log-template.csv`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Open `support-files/scenario/MONITORING_CHECKLIST.md`.
5. Open `support-files/scenario/AUTOMATION_BOUNDARIES.md`.
6. Keep those files available in a separate window or tab while you work.

## Exercise 1: Create the workspace and Lakehouse

In this exercise, you will create the main Module 5 Fabric items and upload the raw files.

### Task 1: Create the workspace

1. Open Microsoft Fabric in your browser.
2. Sign in with your Fabric account.
3. In the left navigation menu, select **Workspaces**.
4. Select **New workspace**.
5. Enter the workspace name `ws_day5_contoso_monitoring`.
6. In the description field, enter `Module 5 performance, monitoring, and automation lab workspace`.
7. Select a licensing mode that supports Fabric capacity in your environment.
8. Create the workspace.
9. When the workspace opens, verify that it is empty.
10. In your learner worksheet, record the workspace name.

### Task 2: Create the Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Enter the name `lh_day5_contoso_runtime`.
4. Create the Lakehouse.
5. Wait until the Lakehouse opens.
6. Confirm that you can see the **Lakehouse explorer** with **Tables** and **Files**.
7. In your worksheet, record the Lakehouse name.

### Task 3: Upload the raw support files

1. In the Lakehouse, open the **Files** area.
2. Create a new folder named `day5-lab`.
3. Open the `day5-lab` folder.
4. Select the upload option.
5. Choose **Upload files**.
6. Browse to the local folder `support-files/data/`.
7. Select these three files:
   - `customers.csv`
   - `products.csv`
   - `orders.csv`
8. Upload the files.
9. Wait until the upload completes.
10. Confirm that all three files are visible in the folder.
11. In your worksheet, record the uploaded file names.
12. In the evidence log, add one row noting that the raw support files are visible in the Lakehouse.

## Exercise 2: Create the notebooks used by the pipeline

In this exercise, you will create the notebooks that the Module 5 pipeline will use.

### Task 1: Create the build notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day5_build_perf_tables`.
5. Open the notebook.
6. Attach the notebook to `lh_day5_contoso_runtime`.
7. Copy the build notebook code block shown below.
8. Paste the code into the first notebook cell.
10. Save the notebook.

Build notebook code:

```python
from pyspark.sql.functions import col, count as spark_count, sum as spark_sum

# Define the Lakehouse Files path that stores the Module 5 source CSV files.
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

### Task 2: Create the fast-check notebook

1. Create another notebook.
2. Name it `nb_day5_fast_metric_check`.
3. Attach the notebook to `lh_day5_contoso_runtime`.
4. Copy the fast-check notebook code block shown below.
5. Paste the code into the notebook.
7. Save the notebook.

Fast-check notebook code:

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

### Task 3: Create the slow-check notebook

1. Create another notebook.
2. Name it `nb_day5_slow_metric_check`.
3. Attach the notebook to `lh_day5_contoso_runtime`.
4. Copy the slow-check notebook code block shown below.
5. Paste the code into the notebook.
7. Save the notebook.

Slow-check notebook code:

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

### Task 4: Create the failing-threshold notebook

1. Create another notebook.
2. Name it `nb_day5_threshold_fail`.
3. Attach the notebook to `lh_day5_contoso_runtime`.
4. Copy the threshold-fail notebook code block shown below.
5. Paste the code into the notebook.
7. Save the notebook.

Threshold-fail notebook code:

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
print("Intentional Module 5 threshold failure for QA monitoring practice.")

# Raise an intentional exception to simulate threshold gate failure.
raise Exception("Intentional Module 5 threshold failure. Replace this notebook with nb_day5_threshold_pass for the rerun.")
```

### Task 5: Create the passing-threshold notebook

1. Create another notebook.
2. Name it `nb_day5_threshold_pass`.
3. Attach the notebook to `lh_day5_contoso_runtime`.
4. Copy the threshold-pass notebook code block shown below.
5. Paste the code into the notebook.
7. Save the notebook.

Threshold-pass notebook code:

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

## Exercise 3: Build the pipeline and inspect the first run

In this exercise, you will create the Module 5 pipeline and run it once with a deliberate threshold failure.

### Task 1: Create the pipeline

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Data pipeline**.
4. Name the pipeline `pl_day5_contoso_monitoring`.
5. Open the pipeline canvas.

### Task 2: Add the notebook activities

1. Add a **Notebook** activity.
2. Name it `Build performance tables`.
3. Select the notebook `nb_day5_build_perf_tables`.
4. Add a second **Notebook** activity.
5. Name it `Fast metric check`.
6. Select the notebook `nb_day5_fast_metric_check`.
7. Add a third **Notebook** activity.
8. Name it `Slow metric check`.
9. Select the notebook `nb_day5_slow_metric_check`.
10. Add a fourth **Notebook** activity.
11. Name it `Threshold gate`.
12. Select the notebook `nb_day5_threshold_fail`.

### Task 3: Connect the activities

1. Connect `Build performance tables` to `Fast metric check` using the success path.
2. Connect `Fast metric check` to `Slow metric check` using the success path.
3. Connect `Slow metric check` to `Threshold gate` using the success path.
4. Save the pipeline.

### Task 4: Run the pipeline

1. Select **Run** or **Run now**.
2. Wait for the run to begin.
3. Confirm that the first three activities succeed.
4. Confirm that the `Threshold gate` activity fails.
5. Open the pipeline run details.
6. Record the overall pipeline status in your worksheet.
7. In the evidence log, add one row for the failed first run.

## Exercise 4: Capture monitoring and performance evidence

In this exercise, you will compare activity durations and identify the failure pattern.

### Task 1: Compare the fast and slow activities

1. In the pipeline run details, open the `Fast metric check` activity.
2. Record the activity duration.
3. Open the `Slow metric check` activity.
4. Record the activity duration.
5. Compare the two durations.
6. Confirm that the slow activity took longer than the fast activity.
7. In your worksheet, write one sentence describing the duration difference.

### Task 2: Capture the failure pattern

1. Open the `Threshold gate` activity details.
2. Read the failure message.
3. Confirm that the earlier activities still succeeded even though the final activity failed.
4. In your worksheet, describe why this is a release-readiness pattern QA should document.

### Task 3: Review Monitoring Hub

1. Open **Monitoring Hub** if it is available in your environment.
2. Filter to the pipeline or notebook items you just ran.
3. Compare the visible fields to `support-files/scenario/MONITORING_CHECKLIST.md`.
4. Record which details you can see, such as:
   - status
   - start time
   - end time
   - duration
5. In the evidence log, add one row for monitoring evidence.

## Exercise 5: Repair the threshold step and rerun

In this exercise, you will switch the threshold notebook to the passing version and rerun the pipeline.

### Task 1: Update the pipeline

1. Return to the pipeline editor.
2. Select the `Threshold gate` activity.
3. Change the notebook from `nb_day5_threshold_fail` to `nb_day5_threshold_pass`.
4. Save the pipeline.

### Task 2: Run the repaired pipeline

1. Run the pipeline again.
2. Wait for all activities to complete.
3. Confirm that the entire pipeline is now successful.
4. Open the second run details.
5. Record the second run status in your worksheet.
6. In the evidence log, add one row for the successful rerun.

### Task 3: Confirm the curated Lakehouse output

1. Open the Lakehouse `lh_day5_contoso_runtime`.
2. Open the **Tables** area.
3. Refresh the explorer if necessary.
4. Confirm that these tables exist:
   - `perf_customers`
   - `perf_products`
   - `perf_orders`
   - `perf_region_sales_summary`
5. If a SQL analytics endpoint is available, run queries to count the tables and inspect `perf_region_sales_summary`.
6. Compare the results to `support-files/scenario/EXPECTED_RESULTS.md`.

## Exercise 6: Create and load the reporting Warehouse

In this exercise, you will create the Warehouse and validate the reporting outputs.

### Task 1: Create the Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name it `wh_day5_contoso_reporting`.
5. Create the Warehouse.
6. Open it.

### Task 2: Create the Warehouse tables

1. Open a new SQL query window.
2. Copy the warehouse table creation script shown below into the SQL editor.
3. Run the script.
4. Confirm that these tables exist:
   - `dbo.DimCustomer`
   - `dbo.DimProduct`
   - `dbo.FactSales`

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

### Task 3: Load the Warehouse data

1. Open a new SQL query window.
2. Copy the warehouse data load script shown below into the SQL editor.
3. Run the script.
4. Wait for the inserts to complete.

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

### Task 4: Validate the SQL outputs

1. Copy the validation queries shown below into a new SQL query window.
2. Run the script.
3. Compare the outputs to `support-files/scenario/EXPECTED_RESULTS.md`.
4. Record the overall total sales, order count, average order value, and regional totals in your worksheet.
5. In the evidence log, add one row for the SQL validation results.

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

## Exercise 7: Prepare the observed-results file for automation

In this exercise, you will convert your Fabric observations into a simple structured file.

### Task 1: Review the automation instructions

1. Open `support-files/automation/README.md`.
2. Read the expected file structure and pytest steps.

### Task 2: Create the observed-results file

1. In the `support-files/automation/` folder, copy `observed_results.template.json`.
2. Name the copy `observed_results.json`.
3. Open `observed_results.json`.
4. Replace the placeholder values with your observed Fabric results:
   - pipeline run statuses
   - fast and slow activity durations
   - whether the slow step was longer than the fast step
   - Warehouse order count
   - total sales
   - average order value
   - region totals
5. Save the file.
6. If you are unsure about value format, open `sample_observed_results.json` and use it as a reference.

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

## Exercise 8: Run the pytest suite

In this exercise, you will run the Module 5 automation checks in a local terminal.

### Task 1: Open the automation folder in a terminal

1. Open a terminal window.
2. Change directory to `support-files/automation/`.

### Task 2: Install pytest if needed

1. If `pytest` is not installed already, run:

```bash
# Install required Python dependencies for local validation tests.
python3 -m pip install -r requirements.txt
```

2. Wait for the installation to complete.

### Task 3: Run the tests

1. Run this command:

```bash
# Run the automated Module 5 result validation test suite.
python3 -m pytest tests/test_day5_results.py
```

2. Review the output.
3. Confirm that all tests pass when your observed results match the expected values.
4. In the evidence log, add one row for the pytest execution result.

## Exercise 9: Classify manual and automated checks

In this exercise, you will separate good automation candidates from checks that should remain manual at first.

### Task 1: Review the automation boundaries

1. Open `support-files/scenario/AUTOMATION_BOUNDARIES.md`.
2. Review the `Automate first` and `Keep manual first` sections.
3. Compare those categories to what you did in the lab.

### Task 2: Complete your summary

1. In your learner worksheet, write one example of a good automation candidate from the lab.
2. Write one example of a check that should remain manual for now.
3. Write one sentence describing why that distinction matters for QA maturity.

## Lab complete

You have now:

- compared fast and slow pipeline behavior
- captured run-history and monitoring evidence
- documented a failure pattern and a successful rerun
- validated reporting outputs with SQL
- populated an observed-results file
- run a first-pass pytest suite against those observed results
