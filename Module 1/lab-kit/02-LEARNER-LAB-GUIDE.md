# Day 1 Lab: Fabric Basics for QA

This lab is designed as a true end-to-end hands-on exercise. You will create a small Microsoft Fabric environment from scratch, load demo data, inspect the key Fabric items, and then validate the environment from a QA point of view.

## Lab scenario

You are part of a QA team validating a customer-specific Microsoft Fabric solution for a fictional retailer named **Contoso Outdoor Retail**.

Your goal in this lab is to create a small demo environment that includes:

- one workspace
- one Lakehouse
- one Warehouse
- one Pipeline
- one semantic layer
- one simple report

You will then inspect those items and record what QA evidence is available in each one.

## Lab objectives

By the end of this lab, you should be able to:

- create and navigate a Fabric workspace at - https://app.fabric.microsoft.com/
- upload files into a Lakehouse and create tables from them
- create and load a Warehouse using SQL
- inspect a pipeline and its run history
- inspect the semantic and report layer
- explain the difference between Lakehouse and Warehouse in QA terms
- identify where QA evidence lives in Fabric

## Estimated time

60 to 75 minutes

## Prerequisites

Before you begin, make sure that:

- you can sign in to Microsoft Fabric - https://app.fabric.microsoft.com/
- you have permission to create items in a Fabric workspace
- you have access to the files in `lab-kit/support-files/`

## Files you will use

Keep these files available during the lab:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/sales_orders.csv`
- `support-files/notebooks/01_load_lakehouse_tables.py`
- `support-files/sql/01_create_warehouse_tables.sql`
- `support-files/sql/02_load_demo_data.sql`
- `support-files/sql/03_validation_queries.sql`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`

## Recommended item names

Use these names during the lab:

- Workspace: `ws_day1_contoso_outdoor`
- Lakehouse: `lh_day1_contoso`
- Warehouse: `wh_day1_contoso`
- Notebook: `nb_day1_load_lakehouse_tables`
- Pipeline: `pl_day1_navigation_demo`
- Report: `rpt_day1_order_status`

## Before you start

1. Open `support-files/templates/learner-worksheet.md`.
2. Open `support-files/templates/evidence-log-template.csv`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Keep those files available in a separate window or tab while you work.

## Exercise 1: Create the workspace and Lakehouse

In this exercise, you will create the Fabric workspace and the Lakehouse that will hold the raw files and tables.

### Task 1: Create the workspace

1. Open Microsoft Fabric in your browser.
2. Sign in with your Fabric account - https://app.fabric.microsoft.com/
3. In the left navigation menu, select **Workspaces**.
4. Select **New workspace**.
5. Enter the workspace name `ws_day1_contoso_outdoor`.
6. In the description field, enter `Day 1 Fabric Basics for QA lab workspace`.
7. Select a licensing mode that supports Fabric capacity in your environment.
8. Create the workspace.
9. When the workspace opens, verify that it is empty.
10. In your learner worksheet, record the workspace name.

### Task 2: Create the Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Enter the name `lh_day1_contoso`.
4. Create the Lakehouse.
5. Wait until the Lakehouse opens.
6. Confirm that you can see the **Lakehouse explorer** with **Tables** and **Files**.
7. In your worksheet, record the Lakehouse name.

## Exercise 2: Upload the demo support files

In this exercise, you will upload the local CSV support files into the Lakehouse so that you can create demo tables.

### Task 1: Create the upload folder

1. In the Lakehouse, open the **Files** area.
2. Open the menu for **Files**.
3. Select the option to create a new folder or subfolder.
4. Create a folder named `day1-lab`.
5. Open the new `day1-lab` folder.

### Task 2: Upload the CSV files

1. In the `day1-lab` folder, select the upload option.
2. Choose **Upload files**.
3. Browse to the local folder `support-files/data/`.
4. Select these three files:
   - `customers.csv`
   - `products.csv`
   - `sales_orders.csv`
5. Upload the files.
6. Wait until the upload completes.
7. Confirm that all three files are visible in the `day1-lab` folder.
8. Open each file preview if your environment allows it.
9. In your worksheet, record the names of the uploaded files.
10. In the evidence log, add one row noting that the raw source files are visible in the Lakehouse.

## Exercise 3: Create Lakehouse tables from the support files

In this exercise, you will use the provided notebook script to create Lakehouse tables from the uploaded CSV files.

### Task 1: Create the notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day1_load_lakehouse_tables`.
5. Open the notebook.

### Task 2: Attach the notebook to the Lakehouse

1. In the notebook, find the Lakehouse attachment selector.
2. Attach the notebook to `lh_day1_contoso`.
3. Confirm that the notebook is now associated with the correct Lakehouse.

### Task 3: Paste and run the notebook code

1. Copy the full notebook code from the inline block below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait for the code to complete successfully.
5. Review the final output, which should show counts for the created tables.

Inline notebook code:

```python
# Day 1 setup notebook
# Attach this notebook to the Lakehouse `lh_day1_contoso`
# before running the code.

from pyspark.sql.functions import col, to_date, when

base_path = "Files/day1-lab"

customers_df = (
    spark.read.option("header", True).csv(f"{base_path}/customers.csv")
    .withColumn("IsActive", when(col("IsActive") == "Y", True).otherwise(False))
)

products_df = (
    spark.read.option("header", True).csv(f"{base_path}/products.csv")
    .withColumn("StandardPrice", col("StandardPrice").cast("double"))
)

sales_orders_df = (
    spark.read.option("header", True).csv(f"{base_path}/sales_orders.csv")
    .withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("OrderAmount", col("OrderAmount").cast("double"))
)

customers_df.write.mode("overwrite").format("delta").saveAsTable("customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("products")
sales_orders_df.write.mode("overwrite").format("delta").saveAsTable("sales_orders")

display(
    spark.sql(
        """
        SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
        UNION ALL
        SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
        UNION ALL
        SELECT 'sales_orders' AS table_name, COUNT(*) AS row_count FROM sales_orders
        """
    )
)
```

### Task 4: Verify the Lakehouse tables

1. Return to the Lakehouse `lh_day1_contoso`.
2. Open the **Tables** area.
3. If the tables do not appear immediately, refresh the Lakehouse explorer.
4. Confirm that these tables exist:
   - `customers`
   - `products`
   - `sales_orders`
5. Open each table and inspect a few rows.
6. In your worksheet, write one sentence describing what the Lakehouse gives QA access to.
7. In the evidence log, add one row noting that the Lakehouse tables are visible.

## Exercise 4: Validate the Lakehouse using SQL

In this exercise, you will query the Lakehouse through the SQL analytics endpoint.

### Task 1: Open the SQL analytics endpoint

1. In the Lakehouse page, switch from the **Lakehouse** view to the **SQL analytics endpoint**.
2. Wait until the SQL interface opens.
3. Open a new SQL query window.

### Task 2: Run the validation queries

1. Copy the `LAKEHOUSE VALIDATION` queries from the inline block below.
2. Paste the queries into the Lakehouse SQL query editor.
3. Run the queries.
4. Review the results carefully.

Inline Lakehouse validation queries:

```sql
SELECT COUNT(*) AS customer_count
FROM customers;

SELECT COUNT(*) AS product_count
FROM products;

SELECT COUNT(*) AS sales_order_count
FROM sales_orders;

SELECT CAST(SUM(OrderAmount) AS DECIMAL(18, 2)) AS total_order_amount
FROM sales_orders;

SELECT
    OrderStatus,
    COUNT(*) AS order_count,
    CAST(SUM(OrderAmount) AS DECIMAL(18, 2)) AS total_order_amount
FROM sales_orders
GROUP BY OrderStatus
ORDER BY OrderStatus;
```

### Task 3: Confirm the expected results

1. Open `support-files/scenario/EXPECTED_RESULTS.md`.
2. Compare your query results to the expected values.
3. Confirm the following:
   - `customers` row count is `6`
   - `products` row count is `6`
   - `sales_orders` row count is `12`
   - total `OrderAmount` is `13276.00`
4. Record the results in your worksheet.
5. In the evidence log, add one row describing the Lakehouse SQL results.

If your environment does not expose the Lakehouse SQL analytics endpoint, record that limitation in your worksheet and continue.

## Exercise 5: Create and load the Warehouse

In this exercise, you will create a Warehouse and load the same business data into relational tables.

### Task 1: Create the Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name the Warehouse `wh_day1_contoso`.
5. Create the Warehouse.
6. Open the Warehouse after it finishes provisioning.
7. In your worksheet, record the Warehouse name.

### Task 2: Create the Warehouse tables

1. In the Warehouse, open a new SQL query window.
2. Copy the full SQL script from the inline block below.
3. Paste the script into the Warehouse SQL editor.
4. Run the script.
5. Refresh the schema browser if necessary.
6. Confirm that these tables exist:
   - `dbo.Customers`
   - `dbo.Products`
   - `dbo.SalesOrders`

Inline Warehouse table creation script:

```sql
DROP TABLE IF EXISTS dbo.SalesOrders;
DROP TABLE IF EXISTS dbo.Products;
DROP TABLE IF EXISTS dbo.Customers;

CREATE TABLE dbo.Customers (
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(200) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    CustomerType VARCHAR(50) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

CREATE TABLE dbo.Products (
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    StandardPrice DECIMAL(18, 2) NOT NULL
);

CREATE TABLE dbo.SalesOrders (
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL,
    OrderStatus VARCHAR(30) NOT NULL
);
```

### Task 3: Load the demo data

1. Open a new SQL query window in the Warehouse.
2. Copy the full SQL script from the inline block below.
3. Paste the script into the Warehouse SQL editor.
4. Run the script.
5. Wait until all insert statements finish successfully.

Inline demo data load script:

```sql
INSERT INTO dbo.Customers (CustomerID, CustomerName, Region, CustomerType, IsActive) VALUES
('C1001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C1002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C1003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C1004', 'City Cycle House', 'East', 'SMB', 'Y'),
('C1005', 'Summit Outdoor Retail', 'North', 'Enterprise', 'Y'),
('C1006', 'Urban Wheels', 'West', 'SMB', 'Y');

INSERT INTO dbo.Products (ProductID, ProductName, Category, StandardPrice) VALUES
('P100', 'Trail Helmet', 'Accessories', 45.00),
('P101', 'Road Bike', 'Bikes', 1200.00),
('P102', 'Mountain Bike', 'Bikes', 1650.00),
('P103', 'Cycling Jersey', 'Apparel', 60.00),
('P104', 'Water Bottle', 'Accessories', 15.00),
('P105', 'Commuter Bike', 'Bikes', 980.00);

INSERT INTO dbo.SalesOrders (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus) VALUES
('SO10001', '2026-01-05', 'C1001', 'P101', 2, 1200.00, 2400.00, 'Shipped'),
('SO10002', '2026-01-06', 'C1002', 'P103', 5, 60.00, 300.00, 'Shipped'),
('SO10003', '2026-01-08', 'C1003', 'P104', 10, 15.00, 150.00, 'Processing'),
('SO10004', '2026-01-10', 'C1004', 'P105', 1, 980.00, 980.00, 'Shipped'),
('SO10005', '2026-01-11', 'C1005', 'P102', 1, 1650.00, 1650.00, 'Processing'),
('SO10006', '2026-01-12', 'C1006', 'P100', 8, 45.00, 360.00, 'Cancelled'),
('SO10007', '2026-01-14', 'C1001', 'P103', 12, 58.00, 696.00, 'Shipped'),
('SO10008', '2026-01-15', 'C1002', 'P101', 1, 1180.00, 1180.00, 'Processing'),
('SO10009', '2026-01-18', 'C1003', 'P105', 2, 950.00, 1900.00, 'Shipped'),
('SO10010', '2026-01-20', 'C1004', 'P104', 20, 14.00, 280.00, 'Shipped'),
('SO10011', '2026-01-22', 'C1005', 'P102', 2, 1600.00, 3200.00, 'Processing'),
('SO10012', '2026-01-25', 'C1006', 'P100', 4, 45.00, 180.00, 'Shipped');
```

## Exercise 6: Validate the Warehouse using SQL

In this exercise, you will confirm that the Warehouse was loaded correctly.

### Task 1: Run the validation queries

1. Open a new SQL query window in the Warehouse.
2. Copy the `WAREHOUSE VALIDATION` queries from the inline block below.
3. Paste the queries into the Warehouse SQL editor.
4. Run the queries.
5. Review the results.

Inline Warehouse validation queries:

```sql
SELECT COUNT(*) AS customer_count
FROM dbo.Customers;

SELECT COUNT(*) AS product_count
FROM dbo.Products;

SELECT COUNT(*) AS sales_order_count
FROM dbo.SalesOrders;

SELECT CAST(SUM(OrderAmount) AS DECIMAL(18, 2)) AS total_order_amount
FROM dbo.SalesOrders;

SELECT
    OrderStatus,
    COUNT(*) AS order_count,
    CAST(SUM(OrderAmount) AS DECIMAL(18, 2)) AS total_order_amount
FROM dbo.SalesOrders
GROUP BY OrderStatus
ORDER BY OrderStatus;

SELECT
    c.Region,
    COUNT(*) AS order_count,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18, 2)) AS total_order_amount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;
```

### Task 2: Compare the results

1. Compare your Warehouse results to `EXPECTED_RESULTS.md`.
2. Confirm that the Warehouse results match the expected counts and totals.
3. Confirm that the Warehouse results also match the Lakehouse results.
4. Record the Warehouse results in your worksheet.
5. In the evidence log, add one row describing the Warehouse query output.
6. In your worksheet, write one sentence describing what the Warehouse gives QA access to.

## Exercise 7: Create a simple Pipeline

In this exercise, you will create a small pipeline so that you can inspect the pipeline item and its run history during the lab.

### Task 1: Create the pipeline

1. Return to the workspace.
2. Select **New item**.
3. Choose **Data pipeline**.
4. Name the pipeline `pl_day1_navigation_demo`.
5. Open the pipeline canvas.

### Task 2: Add two simple activities

1. Add a **Wait** activity to the canvas.
2. Rename it `wait_start`.
3. Set its wait time to `5` seconds.
4. Add a second **Wait** activity to the canvas.
5. Rename it `wait_finish`.
6. Set the second wait time to `3` seconds.
7. Connect `wait_start` to `wait_finish`.
8. Save the pipeline.

If the **Wait** activity is not available in your tenant, use the simplest available activity that can be saved and run successfully.

### Task 3: Run the pipeline

1. Run the pipeline.
2. Wait until the pipeline completes successfully.
3. Open the run history.
4. Confirm that at least one successful run is visible.
5. In your worksheet, record the pipeline name and run status.
6. In the evidence log, add one row describing the pipeline run history.

## Exercise 8: Inspect the semantic layer and create a simple report

In this exercise, you will inspect the Warehouse semantic layer and create one simple report item.

### Task 1: Confirm the default semantic model

1. Return to the workspace.
2. Locate the Warehouse `wh_day1_contoso`.
3. Check whether a default semantic model is visible in the workspace or from the Warehouse experience.
4. Open the semantic model if your environment allows it.
5. Note the tables or fields that are visible.
6. Record one observation about the semantic layer in your worksheet.

### Task 2: Create a simple report

1. Open the Warehouse or the semantic model.
2. Choose the report creation option available in your environment.
3. Use the `SalesOrders` data.
4. Create one simple visual:
   - visual type: clustered column chart
   - axis: `OrderStatus`
   - value: `Sum of OrderAmount`
5. Save the report as `rpt_day1_order_status`.
6. Return to the workspace.
7. Confirm that the report is visible in the workspace item list.
8. Open the report and inspect the visual.
9. Record one observation in your worksheet about what business-facing output is visible.
10. In the evidence log, add one row describing the report or semantic layer evidence.

If your environment does not allow report creation, document that limitation and continue.

## Exercise 9: Perform the Day 1 QA review

In this exercise, you will behave like a QA analyst and review the environment you just created.

### Task 1: Compare Lakehouse and Warehouse

In your worksheet, answer these questions:

1. How is the business data represented in the Lakehouse?
2. How is the same business data represented in the Warehouse?
3. Which environment is better suited for file and table inspection?
4. Which environment is better suited for SQL-based validation?
5. Which environment appears closer to business-facing analytics?

Then write one comparison statement summarizing the difference between Lakehouse and Warehouse in QA terms.

### Task 2: Identify QA evidence sources

Using what you created in the lab, list at least four places where QA evidence can be collected.

Examples include:

- workspace item list
- Lakehouse files
- Lakehouse tables
- Lakehouse SQL results
- Warehouse SQL results
- pipeline run history
- semantic model view
- report output

Record these in your worksheet.

### Task 3: Record customer isolation checks

In your worksheet, answer the following questions:

1. What tells you that this workspace is intended to represent one customer environment?
2. What should QA verify to confirm that another customer cannot access this workspace?
3. What should QA verify to confirm that item permissions behave correctly?
4. What should QA verify to confirm that SQL or report access does not bypass workspace boundaries?

Then write at least three customer-isolation checks.

## Exercise 10: Complete the lab deliverables

Before you finish, verify that your learner worksheet includes:

- workspace name
- Lakehouse name
- Warehouse name
- pipeline name
- visible workspace items
- uploaded file names
- visible Lakehouse tables
- visible Warehouse tables
- Lakehouse query results
- Warehouse query results
- one Lakehouse description in QA terms
- one Warehouse description in QA terms
- one Lakehouse vs. Warehouse comparison statement
- at least three customer-isolation checks

Also verify that your evidence log has at least five completed entries.

## What you should conclude

By the end of this lab, you should be able to say:

- a Fabric solution contains multiple QA validation surfaces
- a Lakehouse and a Warehouse expose different inspection patterns
- a workspace is both a navigation boundary and a customer-isolation clue
- pipeline history, SQL output, semantic models, and reports are all valid QA evidence sources

## Clean up resources

If this was a personal practice environment and you no longer need it:

1. Return to the workspace.
2. Open **Workspace settings**.
3. Locate the workspace removal option.
4. Remove the workspace.

Do not remove the workspace if it is a shared instructor-led environment.

## Troubleshooting

- If the uploaded files do not appear, refresh the Lakehouse file explorer.
- If the Lakehouse tables do not appear after the notebook run, reopen the Lakehouse and refresh the **Tables** area.
- If the Warehouse tables do not appear, rerun `01_create_warehouse_tables.sql`.
- If the Warehouse contains no data, rerun `02_load_demo_data.sql`.
- If your query results do not match `EXPECTED_RESULTS.md`, record the mismatch as a QA finding.
- If your environment does not expose report creation or Lakehouse SQL endpoint features, document the limitation and continue with the remaining exercises.
