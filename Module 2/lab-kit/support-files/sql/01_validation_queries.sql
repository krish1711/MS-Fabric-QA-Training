/* ============================================================
   FULL LOAD VALIDATION
   Run these queries in the Lakehouse SQL analytics endpoint
   ============================================================ */

SELECT COUNT(*) AS bronze_customers_count
FROM bronze_customers;

SELECT COUNT(*) AS bronze_products_count
FROM bronze_products;

SELECT COUNT(*) AS bronze_orders_count
FROM bronze_orders;

SELECT COUNT(*) AS silver_customers_count
FROM silver_customers;

SELECT COUNT(*) AS silver_products_count
FROM silver_products;

SELECT COUNT(*) AS silver_orders_count
FROM silver_orders;

SELECT COUNT(*) AS silver_order_rejections_count
FROM silver_order_rejections;

SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;

SELECT RejectionReason, COUNT(*) AS rejection_count
FROM silver_order_rejections
GROUP BY RejectionReason
ORDER BY RejectionReason;

/* ============================================================
   INCREMENTAL LOAD VALIDATION
   Run these queries after the incremental notebook has run
   ============================================================ */

SELECT COUNT(*) AS silver_orders_count_after_incremental
FROM silver_orders;

SELECT COUNT(*) AS silver_rejections_count_after_incremental
FROM silver_order_rejections;

SELECT COUNT(*) AS accepted_late_arriving_count
FROM silver_orders
WHERE OrderID = 'SO20008';

SELECT COUNT(*) AS duplicate_replay_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20004';

SELECT COUNT(*) AS invalid_status_rejection_count
FROM silver_order_rejections
WHERE OrderID = 'SO20009';

SELECT Region, OrderCount, CAST(TotalOrderAmount AS DECIMAL(18,2)) AS TotalOrderAmount
FROM gold_region_sales_summary
ORDER BY Region;
