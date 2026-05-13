# Day 4 intentional checkpoint failure notebook
# Attach this notebook to the Lakehouse `lh_day4_contoso_ops`
# before running the code.

summary_row_count = spark.sql("SELECT COUNT(*) AS row_count FROM qa_region_sales_summary").collect()[0]["row_count"]

print(f"qa_region_sales_summary row count: {summary_row_count}")
print("Intentional QA checkpoint failure: this notebook is designed to fail so learners can inspect pipeline history.")

raise Exception("Intentional Day 4 QA checkpoint failure. Switch the pipeline to nb_day4_qa_checkpoint_pass for the rerun.")
