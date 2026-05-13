# Day 5 fast metric check notebook
# Attach this notebook to the Lakehouse `lh_day5_contoso_runtime`
# before running the code.

display(
    spark.sql(
        """
        SELECT COUNT(*) AS order_count,
               CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
        FROM perf_orders
        """
    )
)

print("Fast metric check completed.")
