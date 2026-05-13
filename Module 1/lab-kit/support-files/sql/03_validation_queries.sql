/* ============================================================
   LAKEHOUSE VALIDATION
   Run these queries in the Lakehouse SQL analytics endpoint
   ============================================================ */

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

/* ============================================================
   WAREHOUSE VALIDATION
   Run these queries in the Warehouse SQL editor
   ============================================================ */

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
