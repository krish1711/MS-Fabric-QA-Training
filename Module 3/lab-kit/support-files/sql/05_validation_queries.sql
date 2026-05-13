/* ============================================================
   LAKEHOUSE VALIDATION
   Run these in the Lakehouse SQL analytics endpoint
   ============================================================ */

SELECT COUNT(*) AS lake_customers_count
FROM lake_customers;

SELECT COUNT(*) AS lake_products_count
FROM lake_products;

SELECT COUNT(*) AS lake_orders_count
FROM lake_orders;

SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(o.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM lake_orders o
INNER JOIN lake_customers c
    ON o.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

/* ============================================================
   WAREHOUSE BASE VALIDATION
   Run these in the Warehouse SQL editor before MERGE
   ============================================================ */

SELECT COUNT(*) AS warehouse_salesorders_count
FROM dbo.SalesOrders;

SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

/* ============================================================
   CTAS VALIDATION
   Run these in the Warehouse SQL editor before MERGE
   ============================================================ */

SELECT
    Region,
    OrderCount,
    CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.RegionSalesCTAS
ORDER BY Region;

/* ============================================================
   WAREHOUSE POST-MERGE VALIDATION
   Run these after the MERGE script
   ============================================================ */

SELECT COUNT(*) AS warehouse_salesorders_count_after_merge
FROM dbo.SalesOrders;

SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(s.OrderAmount) AS DECIMAL(18,2)) AS TotalOrderAmount
FROM dbo.SalesOrders s
INNER JOIN dbo.Customers c
    ON s.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;

SELECT OrderID, Quantity, OrderAmount, OrderStatus
FROM dbo.SalesOrders
WHERE OrderID IN ('SO30003', 'SO30007')
ORDER BY OrderID;

/* ============================================================
   RECONCILIATION CHECKS
   Use these to compare Warehouse output to the Lakehouse values
   ============================================================ */

SELECT COUNT(*) AS final_order_count_for_reconciliation
FROM dbo.SalesOrders;

SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS final_total_order_amount_for_reconciliation
FROM dbo.SalesOrders;
