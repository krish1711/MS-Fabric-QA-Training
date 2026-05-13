# Day 4 Lab: Pipeline, Semantic Model & Security Testing

This lab is designed as a true end-to-end hands-on exercise. You will upload raw files, build a Fabric pipeline, inspect a controlled failure, rerun the repaired pipeline, validate a Warehouse-backed semantic model, create a report, and test row-level security.

## Lab scenario

You are part of a QA team validating a Fabric reporting solution for **Contoso Outdoor Retail**.

The customer wants daily sales reporting for multiple regions. Your job is to prove that:

- the pipeline runs in the correct sequence
- failures are visible and understandable in run history
- a repaired rerun completes successfully
- the semantic model calculates totals correctly
- the report shows the expected numbers
- restricted users cannot see another region's data

## Lab objectives

By the end of this lab, you should be able to:

- create and run a Fabric pipeline
- inspect partial failure and rerun evidence
- validate curated Lakehouse outputs
- validate semantic model relationships and measures
- validate report KPIs and a region matrix
- create and test RLS roles

## Estimated time

75 to 90 minutes

## Prerequisites

Before you begin, make sure that:

- you can sign in to Microsoft Fabric
- you have permission to create items in a Fabric workspace
- you have access to the files in `lab-kit/support-files/`

## Files you will use

Keep these files available during the lab:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/TEST_MATRIX.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- embedded notebook and SQL code blocks in this guide

## Recommended item names

Use these names during the lab:

- Workspace: `ws_day4_contoso_pipeline_security`
- Lakehouse: `lh_day4_contoso_ops`
- Warehouse: `wh_day4_contoso_reporting`
- Notebook 1: `nb_day4_build_curated_tables`
- Notebook 2: `nb_day4_qa_checkpoint_fail`
- Notebook 3: `nb_day4_qa_checkpoint_pass`
- Pipeline: `pl_day4_contoso_validation`

## Before you start

1. Open `support-files/templates/learner-worksheet.md`.
2. Open `support-files/templates/evidence-log-template.csv`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Open `support-files/scenario/TEST_MATRIX.md`.
5. Keep those files available in a separate window or tab while you work.

## Exercise 1: Create the workspace and Lakehouse

In this exercise, you will create the main Day 4 Fabric items and upload the raw files.

### Task 1: Create the workspace

1. Open Microsoft Fabric in your browser.
2. Sign in with your Fabric account.
3. In the left navigation menu, select **Workspaces**.
4. Select **New workspace**.
5. Enter the workspace name `ws_day4_contoso_pipeline_security`.
6. In the description field, enter `Day 4 pipeline, semantic model, and security testing lab workspace`.
7. Select a licensing mode that supports Fabric capacity in your environment.
8. Create the workspace.
9. When the workspace opens, verify that it is empty.
10. In your learner worksheet, record the workspace name.

### Task 2: Create the Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Enter the name `lh_day4_contoso_ops`.
4. Create the Lakehouse.
5. Wait until the Lakehouse opens.
6. Confirm that you can see the **Lakehouse explorer** with **Tables** and **Files**.
7. In your worksheet, record the Lakehouse name.

### Task 3: Upload the raw support files

1. In the Lakehouse, open the **Files** area.
2. Create a new folder named `day4-lab`.
3. Open the `day4-lab` folder.
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

In this exercise, you will create the notebooks that the pipeline will run.

### Task 1: Create the curated-table notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day4_build_curated_tables`.
5. Open the notebook.
6. Attach the notebook to `lh_day4_contoso_ops`.
7. Copy the curated-table notebook code block shown below.
8. Paste the code into the first notebook cell.
10. Save the notebook.

Curated-table notebook code:

```python
from pyspark.sql.functions import col, count as spark_count, sum as spark_sum

# Define the Lakehouse Files path that stores the Day 4 CSV inputs.
base_path = "Files/day4-lab"

# Load raw CSV sources for customers, products, and orders.
customers_df = spark.read.option("header", True).csv(f"{base_path}/customers.csv")
products_df = spark.read.option("header", True).csv(f"{base_path}/products.csv")
orders_df = spark.read.option("header", True).csv(f"{base_path}/orders.csv")

# Standardize customer columns for curated staging output.
customers_df = customers_df.select(
    col("CustomerID"),
    col("CustomerName"),
    col("Region"),
    col("CustomerSegment"),
    col("IsActive"),
)

# Standardize product columns and cast UnitPrice to decimal.
products_df = products_df.select(
    col("ProductID"),
    col("ProductName"),
    col("Category"),
    col("UnitPrice").cast("decimal(18,2)").alias("UnitPrice"),
    col("IsActive"),
)

# Standardize order columns and cast date/numeric fields to expected data types.
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

# Persist curated staging tables as Delta tables in the Lakehouse.
customers_df.write.mode("overwrite").format("delta").saveAsTable("stg_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("stg_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("stg_orders")

# Build region-level sales summary from orders joined to customers.
summary_df = (
    orders_df.join(customers_df, "CustomerID", "inner")
    .groupBy("Region")
    .agg(
        spark_count("*").alias("OrderCount"),
        spark_sum("OrderAmount").cast("decimal(18,2)").alias("TotalSales"),
    )
    .orderBy("Region")
)

# Save QA summary table used by downstream validation and checkpoint notebooks.
summary_df.write.mode("overwrite").format("delta").saveAsTable("qa_region_sales_summary")

# Validate row counts for all curated/staging tables created in this notebook run.
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

# Preview summary output by region so learners can confirm expected aggregation.
display(spark.sql("SELECT * FROM qa_region_sales_summary ORDER BY Region"))
```

### Task 2: Create the intentional-failure notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day4_qa_checkpoint_fail`.
5. Open the notebook.
6. Attach the notebook to `lh_day4_contoso_ops`.
7. Copy the checkpoint-fail notebook code block shown below.
8. Paste the code into the first notebook cell.
10. Save the notebook.

Checkpoint-fail notebook code:

```python
# Retrieve current row count for the summary table before triggering checkpoint failure.
summary_row_count = spark.sql("SELECT COUNT(*) AS row_count FROM qa_region_sales_summary").collect()[0]["row_count"]

# Print diagnostic output that appears in notebook and pipeline run history.
print(f"qa_region_sales_summary row count: {summary_row_count}")
print("Intentional QA checkpoint failure: this notebook is designed to fail so learners can inspect pipeline history.")

# Raise an intentional exception so learners can test rerun and monitoring flow.
raise Exception("Intentional Lab 4 QA checkpoint failure. Switch the pipeline to nb_day4_qa_checkpoint_pass for the rerun.")
```

### Task 3: Create the successful-checkpoint notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day4_qa_checkpoint_pass`.
5. Open the notebook.
6. Attach the notebook to `lh_day4_contoso_ops`.
7. Copy the checkpoint-pass notebook code block shown below.
8. Paste the code into the first notebook cell.
10. Save the notebook.

Checkpoint-pass notebook code:

```python
# Show final curated regional summary to confirm data readiness on pass path.
display(
    spark.sql(
        """
        SELECT Region, OrderCount, TotalSales
        FROM qa_region_sales_summary
        ORDER BY Region
        """
    )
)

# Print success marker so pipeline logs clearly show checkpoint completion.
print("QA checkpoint passed. Curated tables are available and the pipeline can complete successfully.")
```

## Exercise 3: Build the pipeline and inspect the failure path

In this exercise, you will create a pipeline, run it once with an intentional failure, and inspect the run details.

### Task 1: Create the pipeline

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Data pipeline**.
4. Name the pipeline `pl_day4_contoso_validation`.
5. Open the pipeline canvas.

### Task 2: Add the first notebook activity

1. On the pipeline canvas, add a **Notebook** activity.
2. Name the activity `Build curated tables`.
3. In the activity settings, select the notebook `nb_day4_build_curated_tables`.
4. Save the pipeline.

### Task 3: Add the checkpoint activity

1. Add a second **Notebook** activity to the canvas.
2. Name the activity `QA checkpoint`.
3. In the activity settings, select the notebook `nb_day4_qa_checkpoint_fail`.
4. Connect `Build curated tables` to `QA checkpoint` using the success path.
5. Save the pipeline again.

### Task 4: Run the pipeline

1. Select **Run** or **Run now** on the pipeline.
2. Wait for the run to begin.
3. Confirm that the `Build curated tables` activity succeeds.
4. Confirm that the `QA checkpoint` activity fails.
5. Open the pipeline run history.
6. Select the failed run to inspect the details.
7. Open the failed `QA checkpoint` activity.
8. Read the failure message.
9. In your worksheet, write one sentence describing what failed and why it was expected.
10. In the evidence log, add one row for the failed pipeline run.

## Exercise 4: Repair the pipeline and rerun successfully

In this exercise, you will switch the checkpoint activity to the successful notebook and rerun the pipeline.

### Task 1: Update the checkpoint notebook

1. Return to the pipeline editor.
2. Select the `QA checkpoint` activity.
3. In the activity settings, change the notebook from `nb_day4_qa_checkpoint_fail` to `nb_day4_qa_checkpoint_pass`.
4. Save the pipeline.

### Task 2: Run the repaired pipeline

1. Run the pipeline again.
2. Wait for both activities to complete.
3. Confirm that `Build curated tables` succeeds.
4. Confirm that `QA checkpoint` also succeeds.
5. Open the run history for the second pipeline run.
6. Confirm that the status is fully successful.
7. In your worksheet, record the successful run status.
8. In the evidence log, add one row for the successful rerun.

### Task 3: Validate the Lakehouse curated output

1. Open the Lakehouse `lh_day4_contoso_ops`.
2. Open the **Tables** area.
3. Refresh the explorer if necessary.
4. Confirm that these tables exist:
   - `stg_customers`
   - `stg_products`
   - `stg_orders`
   - `qa_region_sales_summary`
5. Open the SQL analytics endpoint for the Lakehouse if it is available in your environment.
6. Run a query to count rows in each of the three staging tables.
7. Run a query to select all rows from `qa_region_sales_summary`.
8. Compare the outputs to `support-files/scenario/EXPECTED_RESULTS.md`.
9. In your worksheet, write one sentence describing how the Lakehouse output proves that the first activity did useful work even before the failed checkpoint.

## Exercise 5: Create and load the reporting Warehouse

In this exercise, you will create the Warehouse and load the reporting data.

### Task 1: Create the Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name it `wh_day4_contoso_reporting`.
5. Create the Warehouse.
6. Open it after creation.
7. In your worksheet, record the Warehouse name.

### Task 2: Create the Warehouse tables

1. In the Warehouse, open a new SQL query window.
2. Copy the warehouse table creation script shown below.
3. Paste the script into the SQL editor.
4. Run the script.
5. Confirm that these tables now exist:
   - `dbo.DimCustomer`
   - `dbo.DimProduct`
   - `dbo.FactSales`

Warehouse table creation script:

```sql
-- Drop existing fact table first to avoid dependency issues during reset.
IF OBJECT_ID('dbo.FactSales', 'U') IS NOT NULL
    DROP TABLE dbo.FactSales;

-- Drop product dimension if it already exists.
IF OBJECT_ID('dbo.DimProduct', 'U') IS NOT NULL
    DROP TABLE dbo.DimProduct;

-- Drop customer dimension if it already exists.
IF OBJECT_ID('dbo.DimCustomer', 'U') IS NOT NULL
    DROP TABLE dbo.DimCustomer;

-- Create customer dimension table for Warehouse QA validation.
CREATE TABLE dbo.DimCustomer
(
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(100) NOT NULL,
    Region VARCHAR(20) NOT NULL,
    CustomerSegment VARCHAR(30) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

-- Create product dimension table for Warehouse QA validation.
CREATE TABLE dbo.DimProduct
(
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(30) NOT NULL,
    UnitPrice DECIMAL(18,2) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

-- Create sales fact table with transaction-level order records.
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

### Task 3: Load the reporting data

1. Open a new SQL query window.
2. Copy the warehouse data load script shown below.
3. Paste the script into the SQL editor.
4. Run the script.
5. Wait for the inserts to complete successfully.

Warehouse data load script:

```sql
-- Load baseline customer dimension data.
INSERT INTO dbo.DimCustomer (CustomerID, CustomerName, Region, CustomerSegment, IsActive)
VALUES
('C4001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C4002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C4003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C4004', 'City Cycle House', 'East', 'SMB', 'Y'),
('C4005', 'Adventure Works Outlet', 'North', 'SMB', 'Y'),
('C4006', 'Fabrikam Trails', 'West', 'SMB', 'Y');

-- Load baseline product dimension data.
INSERT INTO dbo.DimProduct (ProductID, ProductName, Category, UnitPrice, IsActive)
VALUES
('P400', 'Trail Helmet', 'Accessories', 45.00, 'Y'),
('P401', 'Road Bike', 'Bikes', 1200.00, 'Y'),
('P402', 'Mountain Bike', 'Bikes', 1500.00, 'Y'),
('P403', 'Cycling Jersey', 'Apparel', 60.00, 'Y'),
('P404', 'Water Bottle', 'Accessories', 15.00, 'Y');

-- Load baseline sales fact data used in KPI and regional validation queries.
INSERT INTO dbo.FactSales (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
VALUES
('SO40001', '2026-04-01', 'C4001', 'P401', 1, 1200.00, 1200.00, 'Complete'),
('SO40002', '2026-04-01', 'C4002', 'P403', 4, 60.00, 240.00, 'Complete'),
('SO40003', '2026-04-02', 'C4003', 'P400', 2, 45.00, 90.00, 'Complete'),
('SO40004', '2026-04-02', 'C4004', 'P402', 1, 1500.00, 1500.00, 'Complete'),
('SO40005', '2026-04-03', 'C4005', 'P404', 10, 15.00, 150.00, 'Complete'),
('SO40006', '2026-04-03', 'C4006', 'P401', 1, 1200.00, 1200.00, 'Complete'),
('SO40007', '2026-04-04', 'C4001', 'P403', 3, 60.00, 180.00, 'Complete'),
('SO40008', '2026-04-04', 'C4002', 'P404', 8, 15.00, 120.00, 'Complete');
```

### Task 4: Validate the Warehouse totals

1. Copy the validation queries shown below.
2. Paste them into a new SQL query window.
3. Run the script.
4. Compare the results to `support-files/scenario/EXPECTED_RESULTS.md`.
5. Confirm the overall total sales, overall order count, average order value, and region totals.
6. In the evidence log, add one row for the Warehouse validation query results.

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

-- Validate total sales KPI from fact data.
SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
FROM dbo.FactSales;

-- Validate order volume KPI from fact data.
SELECT COUNT(*) AS order_count
FROM dbo.FactSales;

-- Validate average order value KPI from fact data.
SELECT CAST(AVG(OrderAmount) AS DECIMAL(18,2)) AS average_order_value
FROM dbo.FactSales;

-- Validate regional totals across all regions.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(f.OrderAmount) AS DECIMAL(18,2)) AS TotalSales
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c
    ON f.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

-- Validate North region totals as a filtered assertion.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(f.OrderAmount) AS DECIMAL(18,2)) AS TotalSales
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c
    ON f.CustomerID = c.CustomerID
WHERE c.Region = 'North'
GROUP BY c.Region;

-- Validate West region totals as a filtered assertion.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(f.OrderAmount) AS DECIMAL(18,2)) AS TotalSales
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c
    ON f.CustomerID = c.CustomerID
WHERE c.Region = 'West'
GROUP BY c.Region;
```

## Exercise 6: Validate the semantic model

In this exercise, you will shape the default semantic model and validate the business logic.

### Task 1: Open the default semantic model

1. In the Warehouse, find the default semantic model that was created for reporting.
2. Open the semantic model.
3. Open model view if it is not already visible.

### Task 2: Create the relationships

1. Create a relationship from `FactSales[CustomerID]` to `DimCustomer[CustomerID]`.
2. For this relationship, set:
   - cardinality: many-to-one
   - cross-filter direction: single
   - active relationship: yes
3. Create a relationship from `FactSales[ProductID]` to `DimProduct[ProductID]`.
4. For this relationship, set:
   - cardinality: many-to-one
   - cross-filter direction: single
   - active relationship: yes
5. Save the model.

### Task 3: Create the measures

1. Stay in the semantic model.
2. In the `FactSales` table, create the measure `Total Sales`.
3. Use this DAX formula:

```DAX
Total Sales = SUM(FactSales[OrderAmount])
```

4. Create the measure `Order Count`.
5. Use this DAX formula:

```DAX
Order Count = COUNTROWS(FactSales)
```

6. Create the measure `Average Order Value`.
7. Use this DAX formula:

```DAX
Average Order Value = DIVIDE([Total Sales], [Order Count])
```

8. Save the model again.
9. In your worksheet, record the names of the three measures you created.

## Exercise 7: Build and validate the report

In this exercise, you will create a simple report and validate its outputs.

### Task 1: Create the report

1. Create a new report from the semantic model.
2. Build one report page with these visuals:
   - card visual for `Total Sales`
   - card visual for `Order Count`
   - card visual for `Average Order Value`
   - matrix visual with `DimCustomer[Region]` on rows and `Total Sales` plus `Order Count` in values
3. Save the report.

### Task 2: Validate the report outputs

1. Confirm the unrestricted KPI cards show `4680.00`, `8`, and `585.00`.
2. Confirm the matrix includes all four regions: `East`, `North`, `South`, and `West`.
3. Compare the matrix values by region to `EXPECTED_RESULTS.md`.
4. Confirm that the numbers match exactly.
5. In your worksheet, note any difference you would treat as a test failure.

### Task 3: Validate refresh behavior

1. Trigger a refresh if your environment requires it.
2. Wait for the refresh to complete.
3. Reopen the report.
4. Confirm that the refreshed report still shows the same KPI values and matrix totals.
5. In the evidence log, add one row noting the refresh validation result.

## Exercise 8: Create and test RLS roles

In this exercise, you will create two roles and validate their restricted views.

### Task 1: Create the `NorthRole`

1. In the semantic model, open the security or manage roles area.
2. Create a role named `NorthRole`.
3. On the `DimCustomer` table, apply this DAX table filter:

```DAX
[Region] = "North"
```

4. Save the role.

### Task 2: Create the `WestRole`

1. Create a second role named `WestRole`.
2. On the `DimCustomer` table, apply this DAX table filter:

```DAX
[Region] = "West"
```

3. Save the role.

### Task 3: Test `NorthRole`

1. In the workspace item list, open the semantic model menu (**...**) and select **Security**.
2. On the Security page, locate `NorthRole` and select **Test as role** if this option is available.
3. If **Test as role** is not available in your UI:
   - open **Manage security roles**
   - switch to the **Assign** tab
   - assign a dedicated test user to `NorthRole`
   - make sure that test user has **Viewer** workspace access
   - sign in as that test user and open the report
4. Compare the visible values to `EXPECTED_RESULTS.md`.
5. Confirm that the report shows only North-region data.
6. Confirm that East, South, and West values are not visible.
7. In the evidence log, add one row for the `NorthRole` test.

### Task 4: Test `WestRole`

1. Exit `NorthRole` testing if it is still active.
2. On the semantic model **Security** page, locate `WestRole` and select **Test as role** if this option is available.
3. If **Test as role** is not available in your UI:
   - open **Manage security roles**
   - switch to the **Assign** tab
   - assign the same dedicated test user to `WestRole` for this test
   - sign in as that test user and open the report
4. Compare the visible values to `EXPECTED_RESULTS.md`.
5. Confirm that the report shows only West-region data.
6. Confirm that East, North, and South values are not visible.
7. In the evidence log, add one row for the `WestRole` test.

### Task 5: Return to unrestricted view

1. Select **Back to normal** (or stop role testing) on the security/report test banner.
2. Reopen the report in normal mode.
3. Confirm that the full unrestricted totals return.
4. In your worksheet, write one sentence explaining why this step matters in QA evidence capture.

If you do not see **Security** or **Test as role**, confirm you opened the semantic model menu (not the report menu), and confirm the item is a Power BI semantic model. If your workspace role is read-only, ask your instructor for role-management access. For assignment-based testing, remember that role filtering is validated with a **Viewer** test user.

## Exercise 9: Final QA summary

In this exercise, you will summarize what you proved in the lab.

### Task 1: Complete the learner worksheet

1. Open `support-files/templates/learner-worksheet.md`.
2. Complete the sections for pipeline, semantic model, report, and security validation.
3. Save your notes.

### Task 2: Review the Day 4 test matrix

1. Open `support-files/scenario/TEST_MATRIX.md`.
2. Confirm that you completed at least one check in each category:
   - pipeline execution
   - failure handling
   - semantic model logic
   - report output
   - security isolation

### Task 3: Record the final outcome

1. In your worksheet, write a short conclusion on whether the Day 4 scenario passed or failed QA.
2. If you found any mismatch during the lab, record it as a defect or investigation note.

## Lab complete

You have now:

- created and tested a Fabric pipeline
- observed an intentional pipeline failure and a successful rerun
- validated curated Lakehouse outputs
- validated a Warehouse-backed semantic model
- created and checked a report
- proved row-level security behavior using role-based views
