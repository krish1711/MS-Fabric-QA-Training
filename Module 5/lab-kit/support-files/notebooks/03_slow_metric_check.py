# Day 5 slow metric check notebook
# Attach this notebook to the Lakehouse `lh_day5_contoso_runtime`
# before running the code.

import time

display(
    spark.sql(
        """
        SELECT Region, OrderCount, TotalSales
        FROM perf_region_sales_summary
        ORDER BY Region
        """
    )
)

time.sleep(20)

print("Slow metric check completed after an intentional wait for duration comparison.")
