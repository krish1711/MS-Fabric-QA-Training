# Module 3 Lab: Lakehouse & Warehouse Testing

This lab is designed as a true end-to-end hands-on exercise. You will create a Fabric Lakehouse and Warehouse, generate Delta history in the Lakehouse, create Warehouse outputs using CTAS and MERGE, and then reconcile the final results.

## Lab scenario

You are part of a QA team validating a Fabric solution for **Contoso Outdoor Retail**.

The same customer, product, and order data exists in both a Lakehouse and a Warehouse. Your job is to:

- inspect the Delta-backed Lakehouse tables
- validate the Warehouse using SQL
- prove the CTAS result is correct
- prove the MERGE result is correct
- reconcile Lakehouse and Warehouse outputs

## Lab objectives

By the end of this lab, you should be able to:

- create Delta-backed Lakehouse tables
- inspect Delta history as QA evidence
- create and validate Warehouse tables with SQL
- validate CTAS and MERGE scenarios
- compare Lakehouse and Warehouse outputs confidently
- record SQL-based QA evidence

## Estimated time

60 to 75 minutes

## Prerequisites

Before you begin, make sure that:

- you can sign in to Microsoft Fabric
- you have permission to create items in a Fabric workspace
- you have access to the files in `lab-kit/support-files/`

## Files you will use

Keep these files available during the lab:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders_base.csv`
- `support-files/data/order_updates.csv`
- `support-files/scenario/CHANGE_SCENARIO.md`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- embedded notebook and SQL code blocks in this guide

## Recommended item names

Use these names during the lab:

- Workspace: `ws_day3_contoso_lh_wh`
- Lakehouse: `lh_day3_contoso`
- Warehouse: `wh_day3_contoso`
- Notebook 1: `nb_day3_build_lakehouse_tables`
- Notebook 2: `nb_day3_apply_lakehouse_update`

## Before you start

1. Open `support-files/templates/learner-worksheet.md`.
2. Open `support-files/templates/evidence-log-template.csv`.
3. Open `support-files/scenario/CHANGE_SCENARIO.md`.
4. Open `support-files/scenario/EXPECTED_RESULTS.md`.
5. Keep those files available in a separate window or tab while you work.

## Exercise 1: Create the workspace, Lakehouse, and Warehouse

In this exercise, you will create the main Fabric items for the Module 3 lab.

### Task 1: Create the workspace

1. Open Microsoft Fabric in your browser.
2. Sign in with your Fabric account.
3. In the left navigation menu, select **Workspaces**.
4. Select **New workspace**.
5. Enter the workspace name `ws_day3_contoso_lh_wh`.
6. In the description field, enter `Module 3 Lakehouse and Warehouse Testing lab workspace`.
7. Select a licensing mode that supports Fabric capacity in your environment.
8. Create the workspace.
9. When the workspace opens, verify that it is empty.
10. In your learner worksheet, record the workspace name.

### Task 2: Create the Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Enter the name `lh_day3_contoso`.
4. Create the Lakehouse.
5. Wait until the Lakehouse opens.
6. Confirm that you can see the **Lakehouse explorer** with **Tables** and **Files**.
7. In your worksheet, record the Lakehouse name.

### Task 3: Create the Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Enter the name `wh_day3_contoso`.
5. Create the Warehouse.
6. Open it briefly to confirm that it was created.
7. Return to the workspace.
8. In your worksheet, record the Warehouse name.

## Exercise 2: Upload the support files to the Lakehouse

In this exercise, you will upload the raw CSV support files.

### Task 1: Create the upload folder

1. Open the Lakehouse `lh_day3_contoso`.
2. Open the **Files** area.
3. Open the menu for **Files**.
4. Select the option to create a new folder or subfolder.
5. Create a folder named `day3-lab`.
6. Open the new `day3-lab` folder.

### Task 2: Upload the CSV files

1. In the `day3-lab` folder, select the upload option.
2. Choose **Upload files**.
3. Browse to the local folder `support-files/data/`.
4. Select these four files:
   - `customers.csv`
   - `products.csv`
   - `orders_base.csv`
   - `order_updates.csv`
5. Upload the files.
6. Wait until the upload completes.
7. Confirm that all four files are visible in the folder.
8. In your worksheet, record the uploaded file names.
9. In the evidence log, add one row noting that the raw support files are visible.

## Exercise 3: Create the base Lakehouse Delta tables

In this exercise, you will use the notebook script to create the main Lakehouse tables.

### Task 1: Create the base Lakehouse notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day3_build_lakehouse_tables`.
5. Open the notebook.

### Task 2: Attach the notebook to the Lakehouse

1. In the notebook, find the Lakehouse attachment selector.
2. Attach the notebook to `lh_day3_contoso`.
3. Confirm that the notebook is attached to the correct Lakehouse.

### Task 3: Paste and run the notebook code

1. Copy the Lakehouse base notebook code block shown below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait until the notebook completes successfully.
5. Review the output, which should show the created Lakehouse table counts.

Lakehouse base notebook code:

```python
from pyspark.sql.functions import col, to_date

# Define the Lakehouse Files path that contains the source CSV inputs for this lab.
base_path = "Files/day3-lab"

# Load customer master data from CSV (first row is treated as headers).
customers_df = spark.read.option("header", True).csv(f"{base_path}/customers.csv")
# Load product master data and cast price to numeric for downstream aggregations.
products_df = (
    spark.read.option("header", True).csv(f"{base_path}/products.csv")
    .withColumn("StandardPrice", col("StandardPrice").cast("double"))
)
# Load base order transactions and normalize date/numeric columns to expected types.
orders_df = (
    spark.read.option("header", True).csv(f"{base_path}/orders_base.csv")
    .withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))
    .withColumn("Quantity", col("Quantity").cast("int"))
    .withColumn("UnitPrice", col("UnitPrice").cast("double"))
    .withColumn("OrderAmount", col("OrderAmount").cast("double"))
)

# Save each DataFrame as a managed Delta table in the Lakehouse.
customers_df.write.mode("overwrite").format("delta").saveAsTable("lake_customers")
products_df.write.mode("overwrite").format("delta").saveAsTable("lake_products")
orders_df.write.mode("overwrite").format("delta").saveAsTable("lake_orders")

# Run a quick verification query to confirm row counts in all three Lakehouse tables.
display(
    spark.sql(
        """
        SELECT 'lake_customers' AS table_name, COUNT(*) AS row_count FROM lake_customers
        UNION ALL
        SELECT 'lake_products' AS table_name, COUNT(*) AS row_count FROM lake_products
        UNION ALL
        SELECT 'lake_orders' AS table_name, COUNT(*) AS row_count FROM lake_orders
        """
    )
)
```

### Task 4: Verify the Lakehouse tables

1. Return to the Lakehouse `lh_day3_contoso`.
2. Open the **Tables** area.
3. Refresh the explorer if necessary.
4. Confirm that these tables exist:
   - `lake_customers`
   - `lake_products`
   - `lake_orders`
5. Open the tables and inspect a few rows.
6. In your worksheet, write one sentence describing what the base Lakehouse tables represent in QA terms.

## Exercise 4: Apply the Lakehouse update and inspect Delta history

In this exercise, you will apply a controlled data change to the Lakehouse and then inspect table history.

### Task 1: Review the change scenario

1. Open `support-files/scenario/CHANGE_SCENARIO.md`.
2. Review the update scenario.
3. Confirm that the change scenario includes:
   - one existing order update
   - one new order insert

### Task 2: Create the update notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day3_apply_lakehouse_update`.
5. Open the notebook.

### Task 3: Attach the notebook to the Lakehouse

1. Attach the notebook to `lh_day3_contoso`.
2. Confirm that the correct Lakehouse is attached.

### Task 4: Paste and run the update notebook code

1. Copy the Lakehouse update notebook code block shown below.
2. Paste the code into the first notebook cell.
3. Run the notebook cell.
4. Wait for the notebook to complete successfully.
5. Review the output and note the displayed history information.

Lakehouse update notebook code:

```python
# Update an existing order record to simulate a post-load correction scenario.
spark.sql(
    """
    UPDATE lake_orders
    SET
        Quantity = 5,
        OrderAmount = 225.00,
        OrderStatus = 'Shipped'
    WHERE OrderID = 'SO30003'
    """
)

# Insert a brand-new order record to simulate incremental data arrival.
spark.sql(
    """
    INSERT INTO lake_orders
    VALUES ('SO30007', DATE '2026-03-15', 'C3001', 'P300', 2, 45.00, 90.00, 'Shipped')
    """
)

# Display the full orders table to validate update + insert results.
display(
    spark.sql(
        """
        SELECT OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus
        FROM lake_orders
        ORDER BY OrderID
        """
    )
)

# Show Delta table history so learners can observe recorded write operations.
display(
    spark.sql(
        """
        DESCRIBE HISTORY lake_orders
        """
    )
)
```

### Task 5: Record Lakehouse history observations

1. In your worksheet, record what changed in the Lakehouse orders table.
2. Record how many visible history entries or operations you can observe.
3. In the evidence log, add one row describing the Delta history evidence.

## Exercise 5: Validate the Lakehouse state

In this exercise, you will query the Lakehouse and validate the final post-update state.

### Task 1: Open the Lakehouse SQL analytics endpoint

1. In the Lakehouse page, switch from the **Lakehouse** view to the **SQL analytics endpoint** if available.
2. Wait until the SQL interface opens.
3. Open a new SQL query window.

### Task 2: Run the Lakehouse validation queries

1. Copy the `LAKEHOUSE VALIDATION` queries shown below.
2. Paste the queries into the SQL query editor.
3. Run the queries.
4. Review the results carefully.

Lakehouse validation queries:

```sql
-- Validate Lakehouse customer table row count.
SELECT COUNT(*) AS lake_customers_count
FROM lake_customers;

-- Validate Lakehouse product table row count.
SELECT COUNT(*) AS lake_products_count
FROM lake_products;

-- Validate Lakehouse orders table row count after applying updates.
SELECT COUNT(*) AS lake_orders_count
FROM lake_orders;

-- Validate regional order totals from Lakehouse orders joined to customers.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(o.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM lake_orders o
INNER JOIN lake_customers c
    ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;
```

### Task 3: Compare the results to expected values

1. Open `support-files/scenario/EXPECTED_RESULTS.md`.
2. Compare your results to the expected Lakehouse values.
3. Confirm that:
   - the final `lake_orders` row count is `7`
   - the regional totals match the expected post-update values
4. Record the results in your worksheet.
5. In the evidence log, add one row describing the Lakehouse SQL output.

If your environment does not expose the Lakehouse SQL analytics endpoint, use notebook output and table previews as evidence and continue.

## Exercise 6: Create and load the Warehouse base tables

In this exercise, you will create the Warehouse tables and load the base data.

### Task 1: Create the Warehouse tables

1. Open the Warehouse `wh_day3_contoso`.
2. Open a new SQL query window.
3. Copy the warehouse table creation script shown below.
4. Paste the script into the Warehouse SQL editor.
5. Run the script.
6. Refresh the schema browser if necessary.
7. Confirm that these tables exist:
   - `dbo.Customers`
   - `dbo.Products`
   - `dbo.SalesOrders`
   - `dbo.OrderUpdates`

Warehouse table creation script:

```sql
-- Reset prior demo objects so the table creation script is idempotent.
DROP TABLE IF EXISTS dbo.RegionSalesCTAS;
DROP TABLE IF EXISTS dbo.OrderUpdates;
DROP TABLE IF EXISTS dbo.SalesOrders;
DROP TABLE IF EXISTS dbo.Products;
DROP TABLE IF EXISTS dbo.Customers;

-- Create Warehouse dimension table for customers.
CREATE TABLE dbo.Customers (
    CustomerID VARCHAR(20) NOT NULL,
    CustomerName VARCHAR(200) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    CustomerType VARCHAR(50) NOT NULL,
    IsActive CHAR(1) NOT NULL
);

-- Create Warehouse dimension table for products.
CREATE TABLE dbo.Products (
    ProductID VARCHAR(20) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    Category VARCHAR(100) NOT NULL,
    StandardPrice DECIMAL(18, 2) NOT NULL
);

-- Create Warehouse fact-style table for sales order transactions.
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

-- Create staging/update table that drives the MERGE scenario.
CREATE TABLE dbo.OrderUpdates (
    OrderID VARCHAR(20) NOT NULL,
    OrderDate DATE NOT NULL,
    CustomerID VARCHAR(20) NOT NULL,
    ProductID VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    OrderAmount DECIMAL(18, 2) NOT NULL,
    OrderStatus VARCHAR(30) NOT NULL,
    OperationType VARCHAR(20) NOT NULL
);
```

### Task 2: Load the base data

1. Open a new SQL query window.
2. Copy the warehouse base data load script shown below.
3. Paste the script into the Warehouse SQL editor.
4. Run the script.
5. Wait until the inserts complete successfully.
6. In your worksheet, record that the Warehouse base data was loaded.

Warehouse base data load script:

```sql
-- Load baseline customer rows.
INSERT INTO dbo.Customers (CustomerID, CustomerName, Region, CustomerType, IsActive) VALUES
('C3001', 'Northwind Outfitters', 'North', 'Enterprise', 'Y'),
('C3002', 'Contoso Bikes Store', 'West', 'Enterprise', 'Y'),
('C3003', 'Alpine Sports Hub', 'South', 'SMB', 'Y'),
('C3004', 'City Cycle House', 'East', 'SMB', 'Y');

-- Load baseline product rows.
INSERT INTO dbo.Products (ProductID, ProductName, Category, StandardPrice) VALUES
('P300', 'Trail Helmet', 'Accessories', 45.00),
('P301', 'Road Bike', 'Bikes', 1200.00),
('P302', 'Mountain Bike', 'Bikes', 1500.00),
('P303', 'Cycling Jersey', 'Apparel', 60.00);

-- Load baseline sales order transaction rows.
INSERT INTO dbo.SalesOrders (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus) VALUES
('SO30001', '2026-03-05', 'C3001', 'P301', 2, 1200.00, 2400.00, 'Shipped'),
('SO30002', '2026-03-06', 'C3002', 'P303', 5, 60.00, 300.00, 'Shipped'),
('SO30003', '2026-03-08', 'C3003', 'P300', 4, 45.00, 180.00, 'Processing'),
('SO30004', '2026-03-10', 'C3004', 'P302', 1, 1500.00, 1500.00, 'Shipped'),
('SO30005', '2026-03-11', 'C3001', 'P303', 3, 58.00, 174.00, 'Processing'),
('SO30006', '2026-03-12', 'C3002', 'P300', 6, 45.00, 270.00, 'Shipped');

-- Load change records that will be applied through MERGE (one update, one insert).
INSERT INTO dbo.OrderUpdates (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus, OperationType) VALUES
('SO30003', '2026-03-08', 'C3003', 'P300', 5, 45.00, 225.00, 'Shipped', 'UPDATE'),
('SO30007', '2026-03-15', 'C3001', 'P300', 2, 45.00, 90.00, 'Shipped', 'INSERT');
```

## Exercise 7: Create and validate the CTAS output

In this exercise, you will create a CTAS summary table and validate its results.

### Task 1: Create the CTAS table

1. Open a new SQL query window in the Warehouse.
2. Copy the CTAS script shown below.
3. Paste the script into the Warehouse SQL editor.
4. Run the script.
5. Confirm that the table `dbo.RegionSalesCTAS` exists.

CTAS script:

```sql
-- Recreate the CTAS output table so results reflect current SalesOrders data.
DROP TABLE IF EXISTS dbo.RegionSalesCTAS;

-- Create regional summary table from SalesOrders joined to Customers.
CREATE TABLE dbo.RegionSalesCTAS
AS
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18, 2)) AS TotalOrderAmount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region;
```

### Task 2: Validate the Warehouse base and CTAS output

1. Copy the warehouse base and CTAS validation queries shown below.
2. Paste the queries into the SQL editor and run them.
3. Compare the results with `EXPECTED_RESULTS.md`.
4. Confirm that:
   - the base SalesOrders table has the expected row count
   - the CTAS table has the expected grouped totals
5. Record the results in your worksheet.
6. In the evidence log, add one row describing the CTAS validation evidence.

Warehouse base and CTAS validation queries:

```sql
-- Check baseline Warehouse SalesOrders row count before MERGE.
SELECT COUNT(*) AS warehouse_salesorders_count
FROM dbo.SalesOrders;

-- Validate baseline regional totals directly from base tables.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

-- Validate the same totals from the CTAS output table.
SELECT
    Region,
    OrderCount,
    CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.RegionSalesCTAS
ORDER BY Region;
```

## Exercise 8: Apply and validate the MERGE scenario

In this exercise, you will run a MERGE operation in the Warehouse and validate its effects.

### Task 1: Run the MERGE script

1. Open a new SQL query window in the Warehouse.
2. Copy the MERGE script shown below.
3. Paste the script into the SQL editor.
4. Run the script.
5. Wait until the MERGE completes successfully.

MERGE script:

```sql
-- Apply staged changes to SalesOrders: update existing rows and insert new rows.
MERGE dbo.SalesOrders AS target
USING dbo.OrderUpdates AS source
    ON target.OrderID = source.OrderID
WHEN MATCHED AND source.OperationType = 'UPDATE' THEN
    UPDATE SET
        target.OrderDate = source.OrderDate,
        target.CustomerID = source.CustomerID,
        target.ProductID = source.ProductID,
        target.Quantity = source.Quantity,
        target.UnitPrice = source.UnitPrice,
        target.OrderAmount = source.OrderAmount,
        target.OrderStatus = source.OrderStatus
WHEN NOT MATCHED AND source.OperationType = 'INSERT' THEN
    INSERT (OrderID, OrderDate, CustomerID, ProductID, Quantity, UnitPrice, OrderAmount, OrderStatus)
    VALUES (source.OrderID, source.OrderDate, source.CustomerID, source.ProductID, source.Quantity, source.UnitPrice, source.OrderAmount, source.OrderStatus);
```

### Task 2: Validate the post-MERGE state

1. Copy the post-MERGE and reconciliation queries shown below.
2. Paste them into the SQL editor.
3. Run the queries.
4. Compare the results to `EXPECTED_RESULTS.md`.
5. Confirm that:
   - the final `SalesOrders` row count is `7`
   - the final totals reflect one updated order and one inserted order
6. Record the results in your worksheet.
7. In the evidence log, add one row describing the post-MERGE validation evidence.

Post-MERGE and reconciliation queries:

```sql
-- Check SalesOrders row count after MERGE is applied.
SELECT COUNT(*) AS warehouse_salesorders_count_after_merge
FROM dbo.SalesOrders;

-- Validate post-MERGE regional totals from base Warehouse tables.
SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

-- Inspect the two scenario-specific orders to confirm update and insert effects.
SELECT OrderID, Quantity, OrderAmount, OrderStatus
FROM dbo.SalesOrders
WHERE OrderID IN ('SO30003', 'SO30007')
ORDER BY OrderID;

-- Reconcile final Warehouse row count with Lakehouse final row count.
SELECT COUNT(*) AS final_order_count_for_reconciliation
FROM dbo.SalesOrders;

-- Reconcile final Warehouse order amount total with Lakehouse total.
SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS final_total_order_amount_for_reconciliation
FROM dbo.SalesOrders;
```

## Exercise 9: Reconcile the Lakehouse and Warehouse outputs

In this exercise, you will compare the final outputs from both surfaces.

### Task 1: Review the reconciliation queries

1. Copy the reconciliation queries shown below.
2. Run the Warehouse reconciliation queries.
3. Compare those results with the Lakehouse results you recorded earlier.

Reconciliation queries:

```sql
-- Reconcile final Warehouse row count with Lakehouse final row count.
SELECT COUNT(*) AS final_order_count_for_reconciliation
FROM dbo.SalesOrders;

-- Reconcile final Warehouse order amount total with Lakehouse total.
SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS final_total_order_amount_for_reconciliation
FROM dbo.SalesOrders;
```

### Task 2: Confirm alignment

1. Compare the final row counts between Lakehouse and Warehouse.
2. Compare the final regional totals between Lakehouse and Warehouse.
3. Confirm that the post-MERGE Warehouse values match the post-update Lakehouse values.
4. Record the reconciliation result in your worksheet.
5. In the evidence log, add one row describing the final reconciliation evidence.

## Exercise 10: Complete the Module 3 QA review

In this exercise, you will summarize what happened and turn it into QA findings and test ideas.

### Task 1: Compare Lakehouse and Warehouse in QA terms

In your worksheet, answer the following:

1. What evidence was easiest to collect from the Lakehouse?
2. What evidence was easiest to collect from the Warehouse?
3. What did Delta history prove that a simple row count could not?
4. What did SQL assertions prove in the Warehouse?

Then write one comparison statement summarizing the Lakehouse and Warehouse difference in QA terms.

### Task 2: Record Module 3 test ideas

Write at least five QA test ideas based on this lab. Include examples such as:

- Delta schema validation
- Delta history validation
- Lakehouse row-count validation
- CTAS output validation
- MERGE before-and-after validation
- Lakehouse vs. Warehouse reconciliation

### Task 3: Record evidence sources

List at least five places where QA evidence was collected during the lab.

Examples include:

- file previews
- Lakehouse table previews
- Lakehouse SQL queries
- notebook history output
- Warehouse SQL queries
- CTAS output
- MERGE result

Record these in your worksheet.

## Complete the lab deliverables

Before you finish, verify that your learner worksheet includes:

- workspace, Lakehouse, and Warehouse names
- uploaded file names
- base Lakehouse table observations
- Delta history observations
- Lakehouse validation results
- Warehouse base validation results
- CTAS validation results
- MERGE validation results
- reconciliation results
- one Lakehouse vs. Warehouse comparison statement
- at least five test ideas
- at least five QA evidence sources

Also verify that your evidence log has at least five completed entries.

## What you should conclude

By the end of this lab, you should be able to say:

- Delta tables give QA more than just table contents; they also give history evidence
- Warehouse SQL scripts are useful as reusable validation assets
- CTAS and MERGE are testable behaviors, not just implementation details
- reconciliation between Lakehouse and Warehouse is a high-value QA activity

## Clean up resources

If this was a personal practice environment and you no longer need it:

1. Return to the workspace.
2. Open **Workspace settings**.
3. Locate the workspace removal option.
4. Remove the workspace.

Do not remove the workspace if it is a shared instructor-led environment.

## Troubleshooting

- If the uploaded files do not appear, refresh the Lakehouse file explorer.
- If the Lakehouse tables do not appear after the notebook run, refresh the **Tables** area.
- If the Warehouse tables do not appear, rerun the table creation script from Exercise 6, Task 1.
- If the CTAS table is missing, rerun the CTAS script from Exercise 7, Task 1.
- If the MERGE results do not match expectations, rerun the base load script from Exercise 6, Task 2 and then rerun the MERGE script from Exercise 8, Task 1.
- If the SQL endpoint is unavailable in your environment, use notebook outputs and table previews as evidence and continue.
