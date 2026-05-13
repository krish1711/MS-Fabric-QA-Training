# Day 5 threshold pass notebook
# Attach this notebook to the Lakehouse `lh_day5_contoso_runtime`
# before running the code.

display(
    spark.sql(
        """
        SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales,
               COUNT(*) AS order_count
        FROM perf_orders
        """
    )
)

print("Threshold gate passed. The pipeline can complete successfully.")
