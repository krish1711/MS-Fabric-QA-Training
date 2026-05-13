# Day 5 threshold fail notebook
# Attach this notebook to the Lakehouse `lh_day5_contoso_runtime`
# before running the code.

total_sales = spark.sql(
    """
    SELECT CAST(SUM(OrderAmount) AS DECIMAL(18,2)) AS total_sales
    FROM perf_orders
    """
).collect()[0]["total_sales"]

print(f"Observed total sales: {total_sales}")
print("Intentional Day 5 threshold failure for QA monitoring practice.")

raise Exception("Intentional Day 5 threshold failure. Replace this notebook with nb_day5_threshold_pass for the rerun.")
