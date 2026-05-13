# Instructor Setup Guide

This guide prepares the Day 4 lab environment from top to bottom.

Follow these steps in order.

## 1. What You Will Build

By the end of setup, your environment should contain:

- one Fabric workspace
- one Lakehouse with uploaded raw files
- three notebooks for pipeline setup and checkpoint behavior
- one pipeline with an intentional failure path and a successful rerun path
- one Warehouse with reporting tables
- one Warehouse default semantic model shaped for reporting
- one simple report
- two RLS roles validated through View as

## 2. Before You Start

Make sure you have:

- access to Microsoft Fabric
- permission to create a workspace, Lakehouse, Warehouse, notebook, pipeline, semantic model changes, and reports
- access to the files in this `lab-kit/support-files/` folder

Files you will use during setup:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/TEST_MATRIX.md`
- embedded notebook and SQL code blocks in this guide

## 3. Review the Scenario Files

Before building the environment:

1. Open `support-files/scenario/SCENARIO.md`.
2. Open `support-files/scenario/DATA_DICTIONARY.md`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Open `support-files/scenario/TEST_MATRIX.md`.
5. Confirm that the expected totals and RLS outcomes match the teaching story you want to use.

## 4. Create the Demo Workspace

1. Sign in to Microsoft Fabric.
2. Open **Workspaces**.
3. Select **New workspace**.
4. Enter the name `ws_day4_contoso_pipeline_security`.
5. Add a description such as `Day 4 Pipeline, Semantic Model, and Security Testing lab workspace`.
6. Select a licensing mode that supports Fabric capacity.
7. Create the workspace.
8. Open the new workspace.

## 5. Create the Demo Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Name the Lakehouse `lh_day4_contoso_ops`.
4. Create the Lakehouse.
5. Open the new Lakehouse.

## 6. Upload the Support Files

1. In the Lakehouse, open the **Files** area.
2. Create a folder named `day4-lab`.
3. Open the `day4-lab` folder.
4. Upload these files from `support-files/data/`:
   - `customers.csv`
   - `products.csv`
   - `orders.csv`
5. Confirm that all three files are visible after the upload completes.

## 7. Create the Notebooks

### Notebook 1: Build curated tables

1. Return to the workspace.
2. Select **New item**.
3. Choose **Notebook**.
4. Name it `nb_day4_build_curated_tables`.
5. Attach the notebook to `lh_day4_contoso_ops`.
6. Copy the curated-table notebook code block shown below into the notebook.
8. Save the notebook.

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

# Preview summary output by region so instructors can confirm expected aggregation.
display(spark.sql("SELECT * FROM qa_region_sales_summary ORDER BY Region"))
```

### Notebook 2: Intentional checkpoint failure

1. Create another notebook.
2. Name it `nb_day4_qa_checkpoint_fail`.
3. Attach the notebook to `lh_day4_contoso_ops`.
4. Copy the checkpoint-fail notebook code block shown below into the notebook.
6. Save the notebook.

Checkpoint-fail notebook code:

```python
# Retrieve current row count for the summary table before triggering checkpoint failure.
summary_row_count = spark.sql("SELECT COUNT(*) AS row_count FROM qa_region_sales_summary").collect()[0]["row_count"]

# Print diagnostic output that appears in notebook and pipeline run history.
print(f"qa_region_sales_summary row count: {summary_row_count}")
print("Intentional QA checkpoint failure: this notebook is designed to fail so learners can inspect pipeline history.")

# Raise an intentional exception so learners can test rerun and monitoring flow.
raise Exception("Intentional Day 4 QA checkpoint failure. Switch the pipeline to nb_day4_qa_checkpoint_pass for the rerun.")
```

### Notebook 3: Successful checkpoint

1. Create another notebook.
2. Name it `nb_day4_qa_checkpoint_pass`.
3. Attach the notebook to `lh_day4_contoso_ops`.
4. Copy the checkpoint-pass notebook code block shown below into the notebook.
6. Save the notebook.

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

## 8. Create the Demo Pipeline

1. In the workspace, select **New item**.
2. Choose **Data pipeline**.
3. Name the pipeline `pl_day4_contoso_validation`.
4. Open the pipeline canvas.
5. Add a **Notebook** activity.
6. Name the activity `Build curated tables`.
7. Configure it to run `nb_day4_build_curated_tables`.
8. Add a second **Notebook** activity.
9. Name the activity `QA checkpoint`.
10. Configure it to run `nb_day4_qa_checkpoint_fail`.
11. Connect `Build curated tables` to `QA checkpoint` using the success path.
12. Save the pipeline.

## 9. Run the Pipeline and Confirm the Intentional Failure

1. Run the pipeline.
2. Wait for the first activity to complete.
3. Confirm that the second activity fails.
4. Open the pipeline run details.
5. Capture the failure message from the `QA checkpoint` notebook.
6. Confirm that the first activity succeeded and the second activity failed.
7. Open the Lakehouse and verify that these tables now exist:
   - `stg_customers`
   - `stg_products`
   - `stg_orders`
   - `qa_region_sales_summary`

## 10. Repair the Pipeline for the Successful Rerun

1. Return to the pipeline editor.
2. Open the `QA checkpoint` activity settings.
3. Change the notebook selection from `nb_day4_qa_checkpoint_fail` to `nb_day4_qa_checkpoint_pass`.
4. Save the pipeline.
5. Run the pipeline again.
6. Wait until both activities complete successfully.
7. Open the second pipeline run history and confirm that the full pipeline is now successful.

## 11. Validate the Lakehouse Curated Output

1. Open the Lakehouse SQL analytics endpoint if available.
2. Open `support-files/scenario/EXPECTED_RESULTS.md`.
3. Confirm that the Day 4 Lakehouse expectations are visible.
4. Run these checks in the SQL endpoint:
   - count rows in `stg_customers`
   - count rows in `stg_products`
   - count rows in `stg_orders`
   - query `qa_region_sales_summary`
5. Compare the query outputs to the expected results document.

## 12. Create the Demo Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name the Warehouse `wh_day4_contoso_reporting`.
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

## 14. Validate the Reporting Data

1. Copy the validation queries shown below.
2. Run the full script in the Warehouse.
3. Compare the results to `EXPECTED_RESULTS.md`.
4. Confirm the total sales, order count, average order value, and region totals.

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

## 15. Shape the Semantic Model

1. In the Warehouse, open the default semantic model.
2. Create these relationships:
   - `FactSales[CustomerID]` to `DimCustomer[CustomerID]`
   - `FactSales[ProductID]` to `DimProduct[ProductID]`
3. Confirm that both relationships use:
   - cardinality: many-to-one
   - cross-filter direction: single
   - active relationship: yes
4. Create these DAX measures in `FactSales`:
   - `Total Sales = SUM(FactSales[OrderAmount])`
   - `Order Count = COUNTROWS(FactSales)`
   - `Average Order Value = DIVIDE([Total Sales], [Order Count])`
5. Save the semantic model changes.

## 16. Build and Validate the Report

1. Create a report from the semantic model.
2. Build one report page with these visuals:
   - card visual for `Total Sales`
   - card visual for `Order Count`
   - card visual for `Average Order Value`
   - matrix visual with `DimCustomer[Region]` on rows and `Total Sales` plus `Order Count` in values
3. Confirm the unrestricted KPI cards show `4680.00`, `8`, and `585.00`.
4. Confirm the matrix includes `East`, `North`, `South`, and `West`.
5. Compare the report outputs to `EXPECTED_RESULTS.md`.
6. Trigger a refresh if your environment requires it.
7. Confirm that the refreshed report still matches expected totals.

## 17. Create and Test RLS Roles

1. In the semantic model, open the roles/security area.
2. Create the role `NorthRole` and apply this `DimCustomer` filter:
   - `[Region] = "North"`
3. Create the role `WestRole` and apply this `DimCustomer` filter:
   - `[Region] = "West"`
4. Open the semantic model menu (**...**) in the workspace and select **Security**.
5. Use **Test as role** for `NorthRole` if available, and confirm that only North-region rows are visible.
6. Use **Test as role** for `WestRole` if available, and confirm that only West-region rows are visible.
7. If **Test as role** is not available, open **Manage security roles** -> **Assign**, assign a dedicated Viewer test user to each role, and validate by opening the report as that test user.
8. Confirm that East and South rows are not visible in either restricted role.
9. Clear role testing (**Back to normal**) and confirm unrestricted totals return.

## 18. Final Instructor Validation Checklist

Before learners begin, confirm that:

- the workspace `ws_day4_contoso_pipeline_security` exists
- the Lakehouse `lh_day4_contoso_ops` exists
- the uploaded files are visible in `Files/day4-lab`
- the three notebooks exist and are attached to the Lakehouse
- the pipeline exists
- one failed pipeline run is visible
- one successful rerun is visible
- the curated Lakehouse tables exist
- the Warehouse exists and is loaded
- the semantic model contains the required relationships and measures
- the report totals match the expected results
- `NorthRole` and `WestRole` produce the expected restricted views

## 19. Files to Share with Learners

Share or point learners to these files:

- `02-LEARNER-LAB-GUIDE.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/TEST_MATRIX.md`

## 20. Troubleshooting Notes

- If the pipeline activity cannot find the notebook, confirm that the notebook is saved and attached to the correct Lakehouse.
- If the first pipeline run does not fail, make sure the `QA checkpoint` activity still points to `nb_day4_qa_checkpoint_fail`.
- If the second pipeline run still fails, confirm that the notebook reference was switched to `nb_day4_qa_checkpoint_pass`.
- If the Warehouse totals do not match expectations, rerun the create and load scripts in order.
- If report visuals look empty after RLS testing, clear **View as** before validating the unrestricted report again.
