/* ============================================================
   COUNT VALIDATION
   ============================================================ */

SELECT COUNT(*) AS dimcustomer_count
FROM dbo.DimCustomer;

SELECT COUNT(*) AS dimproduct_count
FROM dbo.DimProduct;

SELECT COUNT(*) AS factsales_count
FROM dbo.FactSales;

/* ============================================================
   KPI VALIDATION
   ============================================================ */

SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
FROM dbo.FactSales;

SELECT COUNT(*) AS order_count
FROM dbo.FactSales;

SELECT CAST(AVG(OrderAmount) AS DECIMAL(18,2)) AS average_order_value
FROM dbo.FactSales;

/* ============================================================
   REGION VALIDATION
   ============================================================ */

SELECT
    c.Region,
    COUNT(*) AS OrderCount,
    CAST(SUM(f.OrderAmount) AS DECIMAL(18,2)) AS TotalSales
FROM dbo.FactSales f
INNER JOIN dbo.DimCustomer c
    ON f.CustomerID = c.CustomerID
GROUP BY c.Region
ORDER BY c.Region;
