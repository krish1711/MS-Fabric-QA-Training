# Instructor Setup Guide

This guide prepares the Day 3 lab environment from top to bottom.

Follow these steps in order.

## 1. What You Will Build

By the end of setup, your environment should contain:

- one Fabric workspace
- one Lakehouse with Delta-backed tables
- one Lakehouse update notebook run to create Delta history
- one Warehouse loaded with the same business data
- one CTAS output table
- one MERGE scenario applied in the Warehouse

## 2. Before You Start

Make sure you have:

- access to Microsoft Fabric
- permission to create a workspace, Lakehouse, Warehouse, and notebooks
- access to the files in this `lab-kit/support-files/` folder

Files you will use during setup:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/orders_base.csv`
- `support-files/data/order_updates.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/CHANGE_SCENARIO.md`
- embedded notebook and SQL code blocks in this guide

## 3. Review the Scenario Files

Before building the environment:

1. Open `support-files/scenario/SCENARIO.md`.
2. Open `support-files/scenario/DATA_DICTIONARY.md`.
3. Open `support-files/scenario/CHANGE_SCENARIO.md`.
4. Open `support-files/scenario/EXPECTED_RESULTS.md`.
5. Confirm that the change scenario and expected results match the story you want to teach.

## 4. Create the Demo Workspace

1. Sign in to Microsoft Fabric.
2. Open **Workspaces**.
3. Select **New workspace**.
4. Enter the name `ws_day3_contoso_lh_wh`.
5. Add a description such as `Day 3 Lakehouse and Warehouse Testing lab workspace`.
6. Select a licensing mode that supports Fabric capacity.
7. Create the workspace.
8. Open the new workspace.

## 5. Create the Demo Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Name the Lakehouse `lh_day3_contoso`.
4. Create the Lakehouse.
5. Open the new Lakehouse.

## 6. Upload the Support Files

1. In the Lakehouse, open the **Files** area.
2. Create a folder named `day3-lab`.
3. Open the `day3-lab` folder.
4. Upload these files from `support-files/data/`:
   - `customers.csv`
   - `products.csv`
   - `orders_base.csv`
   - `order_updates.csv`
5. Confirm that all four files are visible after the upload completes.

## 7. Create the Lakehouse Base Notebook

1. Return to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day3_build_lakehouse_tables`.
5. Open the notebook.
6. Attach the notebook to `lh_day3_contoso`.
7. Copy the Lakehouse base notebook code block shown below.
8. Paste the contents into the first notebook cell.
9. Run the notebook.
10. Wait until it completes successfully.
11. Return to the Lakehouse and confirm that these tables exist:
    - `lake_customers`
    - `lake_products`
    - `lake_orders`

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

## 8. Create the Lakehouse Update Notebook

1. Return to the workspace.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day3_apply_lakehouse_update`.
5. Open the notebook.
6. Attach the notebook to `lh_day3_contoso`.
7. Copy the Lakehouse update notebook code block shown below.
8. Paste the contents into the first notebook cell.
9. Run the notebook.
10. Wait until it completes successfully.
11. Review the notebook output and confirm that table history information is displayed.

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

## 9. Validate the Lakehouse State

1. Open the Lakehouse SQL analytics endpoint if available.
2. Copy the `LAKEHOUSE VALIDATION` queries shown below.
3. Paste them into the SQL analytics endpoint query window.
4. Run the queries.
5. Compare the results with `EXPECTED_RESULTS.md`.
6. Confirm that:
   - `lake_customers` row count is `4`
   - `lake_products` row count is `4`
   - `lake_orders` row count after the Lakehouse update is `7`
   - regional totals match the expected final Lakehouse summary

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

## 10. Create the Demo Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name the Warehouse `wh_day3_contoso`.
5. Create the Warehouse.
6. Open the new Warehouse.

## 11. Create Warehouse Tables

1. In the Warehouse, open a new SQL query window.
2. Copy the warehouse table creation script shown below.
3. Paste the script into the query editor.
4. Run the script.
5. Confirm that these tables exist:
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

## 12. Load the Warehouse Base Data

1. Open a new SQL query window in the Warehouse.
2. Copy the warehouse base data load script shown below.
3. Paste the script into the query editor.
4. Run the script.
5. Wait until the inserts complete successfully.

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

## 13. Create the CTAS Output Table

1. Open a new SQL query window in the Warehouse.
2. Copy the CTAS script shown below.
3. Paste the script into the query editor.
4. Run the script.
5. Confirm that the table `dbo.RegionSalesCTAS` now exists.

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

## 14. Validate the Warehouse Base and CTAS State

1. Copy the warehouse base and CTAS validation queries shown below.
2. Paste them into the Warehouse query editor.
3. Run the queries.
4. Compare the results with `EXPECTED_RESULTS.md`.
5. Confirm that the base Warehouse totals and CTAS output match the expected pre-MERGE values.

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

## 15. Apply the MERGE Scenario

1. Open a new SQL query window in the Warehouse.
2. Copy the MERGE script shown below.
3. Paste the script into the query editor.
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

## 16. Validate the Post-MERGE State

1. Copy the post-MERGE and reconciliation queries shown below.
2. Paste them into the Warehouse query editor.
3. Run the queries.
4. Compare the results with `EXPECTED_RESULTS.md`.
5. Confirm that the post-MERGE Warehouse outputs now match the final Lakehouse outputs.

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

## 17. Final Instructor Validation Checklist

Before the learners begin, confirm that:

- the workspace `ws_day3_contoso_lh_wh` exists
- the Lakehouse `lh_day3_contoso` exists
- the Warehouse `wh_day3_contoso` exists
- the uploaded files are visible in `Files/day3-lab`
- the Lakehouse tables exist
- the Lakehouse update notebook has been run
- Delta history output is visible from the Lakehouse update notebook
- the Warehouse tables exist and are loaded
- the CTAS table exists
- the MERGE script has been run
- the validation queries match the expected results document

## 18. Files to Share with Learners

Share or point learners to these files:

- `02-LEARNER-LAB-GUIDE.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- `support-files/scenario/EXPECTED_RESULTS.md`
- `support-files/scenario/CHANGE_SCENARIO.md`

## 19. Troubleshooting Notes

- If the Lakehouse tables do not appear, refresh the Lakehouse explorer after each notebook run.
- If Delta history does not look visible in the notebook output, rerun the Lakehouse update notebook.
- If the Warehouse tables are missing, rerun the table creation script from section 11.
- If the CTAS table is missing, rerun the CTAS script from section 13.
- If the MERGE results do not match expectations, rerun the base load script from section 12 and then rerun the MERGE script from section 15.
