# Day 4 successful checkpoint notebook
# Attach this notebook to the Lakehouse `lh_day4_contoso_ops`
# before running the code.

display(
    spark.sql(
        """
        SELECT Region, OrderCount, TotalSales
        FROM qa_region_sales_summary
        ORDER BY Region
        """
    )
)

print("QA checkpoint passed. Curated tables are available and the pipeline can complete successfully.")
