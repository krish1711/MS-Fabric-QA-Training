DROP TABLE IF EXISTS dbo.RegionSalesCTAS;

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
