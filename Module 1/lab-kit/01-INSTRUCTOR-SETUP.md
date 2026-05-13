# Instructor Setup Guide

This guide prepares the Day 1 lab environment from top to bottom.

Follow these steps in order.

## 1. What You Will Build

By the end of setup, your workspace should contain:

- One Lakehouse loaded with demo files and demo tables
- One Warehouse loaded with the same demo data
- One simple Data pipeline with at least one successful run
- One default semantic model from the Warehouse
- One simple report saved in the workspace

## 2. Before You Start

Make sure you have:

- Access to a Microsoft Fabric workspace where you can create items
- Permission to create a Lakehouse, Warehouse, Pipeline, and Report
- Access to the files in this lab kit folder

Files you will use during setup:

- `support-files/data/customers.csv`
- `support-files/data/products.csv`
- `support-files/data/sales_orders.csv`
- `support-files/notebooks/01_load_lakehouse_tables.py`
- `support-files/sql/01_create_warehouse_tables.sql`
- `support-files/sql/02_load_demo_data.sql`
- `support-files/sql/03_validation_queries.sql`
- `support-files/scenario/EXPECTED_RESULTS.md`

## 3. Review the Support Files

Before you start building the demo environment:

1. Open `support-files/scenario/SCENARIO.md`.
2. Open `support-files/scenario/DATA_DICTIONARY.md`.
3. Open `support-files/scenario/EXPECTED_RESULTS.md`.
4. Confirm that the support files match the scenario you want to teach.

## 4. Create the Demo Workspace

1. Sign in to Microsoft Fabric.
2. In the left navigation, open **Workspaces**.
3. Select **New workspace**.
4. Enter the name `ws_day1_contoso_outdoor`.
5. Add a short description such as `Day 1 Fabric Basics for QA demo workspace`.
6. Save the workspace.
7. Open the new workspace.

## 5. Create the Demo Lakehouse

1. Inside the workspace, select **New item**.
2. Choose **Lakehouse**.
3. Name the Lakehouse `lh_day1_contoso`.
4. Create the item.
5. Open the new Lakehouse.

## 6. Upload the CSV Support Files to the Lakehouse

1. In the Lakehouse, open the **Files** area.
2. Create a folder named `day1-lab`.
3. Open the `day1-lab` folder.
4. Upload these three files from `support-files/data/`:
   - `customers.csv`
   - `products.csv`
   - `sales_orders.csv`
5. Confirm that all three files appear in the folder after the upload completes.

## 7. Create Lakehouse Tables Using the Notebook Script

This step gives the learners both file-level and table-level assets to inspect.

1. Go back to the workspace home page.
2. Select **New item**.
3. Choose **Notebook**.
4. Name the notebook `nb_day1_load_lakehouse_tables`.
5. Open the notebook.
6. Attach the notebook to the Lakehouse `lh_day1_contoso`.
7. Open the local file `support-files/notebooks/01_load_lakehouse_tables.py`.
8. Copy the full contents of that file.
9. Paste the code into the first notebook cell.
10. Run the notebook.
11. Wait for the notebook to finish successfully.
12. Return to the Lakehouse.
13. Open the **Tables** area.
14. Confirm that these tables exist:
    - `customers`
    - `products`
    - `sales_orders`

## 8. Validate the Lakehouse Load

1. Open the SQL analytics endpoint for the Lakehouse if it is available in your environment.
2. Open the local file `support-files/sql/03_validation_queries.sql`.
3. Copy the queries from the section named `LAKEHOUSE VALIDATION`.
4. Paste them into the SQL analytics endpoint query editor.
5. Run the queries.
6. Compare the results with `support-files/scenario/EXPECTED_RESULTS.md`.
7. Confirm that:
   - `customers` row count is `6`
   - `products` row count is `6`
   - `sales_orders` row count is `12`
   - total `OrderAmount` is `13276.00`

## 9. Create the Demo Warehouse

1. Return to the workspace.
2. Select **New item**.
3. Choose **Warehouse**.
4. Name the Warehouse `wh_day1_contoso`.
5. Create the item.
6. Open the new Warehouse.

## 10. Create Warehouse Tables

1. In the Warehouse, open a new SQL query window.
2. Open the local file `support-files/sql/01_create_warehouse_tables.sql`.
3. Copy the full contents of the script.
4. Paste the script into the query editor.
5. Run the script.
6. Confirm that the tables were created:
   - `dbo.Customers`
   - `dbo.Products`
   - `dbo.SalesOrders`

## 11. Load the Demo Data into the Warehouse

1. Open a new SQL query window in the Warehouse.
2. Open the local file `support-files/sql/02_load_demo_data.sql`.
3. Copy the full contents of the script.
4. Paste the script into the query editor.
5. Run the script.
6. Wait for the insert statements to complete.

## 12. Validate the Warehouse Load

1. Open a new SQL query window in the Warehouse.
2. Open the local file `support-files/sql/03_validation_queries.sql`.
3. Copy the queries from the section named `WAREHOUSE VALIDATION`.
4. Paste them into the Warehouse query editor.
5. Run the queries.
6. Compare the results with `support-files/scenario/EXPECTED_RESULTS.md`.
7. Confirm that the Warehouse results match the Lakehouse results.

## 13. Create a Simple Pipeline for Day 1 Navigation

The Day 1 lab only needs a pipeline item and one successful run so learners can inspect the item and its run history.

1. Return to the workspace.
2. Select **New item**.
3. Choose **Data pipeline**.
4. Name the pipeline `pl_day1_navigation_demo`.
5. Open the pipeline canvas.
6. Add a **Wait** activity and name it `wait_start`.
7. Set the wait time to `5` seconds.
8. Add a second **Wait** activity and name it `wait_finish`.
9. Set the second wait time to `3` seconds.
10. Connect `wait_start` to `wait_finish`.
11. Save the pipeline.
12. Run the pipeline once.
13. Wait until the run completes successfully.
14. Confirm that the run history is visible.

If your tenant does not expose a **Wait** activity, create the simplest available pipeline activity that can be saved and run successfully.

## 14. Confirm the Default Semantic Model

1. Return to the workspace.
2. Locate the Warehouse `wh_day1_contoso`.
3. Confirm that a default semantic model is present in the workspace item list or available from the Warehouse experience.

If the default semantic model is not visible immediately, refresh the workspace after the Warehouse load is complete.

## 15. Create a Simple Report

This step is recommended so learners can inspect a report item, but the lab can still run if this step is skipped.

1. Open the Warehouse `wh_day1_contoso`.
2. Choose the report creation option available in your tenant.
   - Common labels include `New report`, `Create report`, or a report action from the Warehouse or semantic model.
3. Use the `SalesOrders` table from the default semantic model.
4. Create one simple visual:
   - Visual type: clustered column chart
   - Axis: `OrderStatus`
   - Value: `Sum of OrderAmount`
5. Save the report as `rpt_day1_order_status`.
6. Return to the workspace and confirm that the report appears.

## 16. Final Instructor Validation Checklist

Before the learners start, confirm that the workspace contains:

- `lh_day1_contoso`
- `wh_day1_contoso`
- `pl_day1_navigation_demo`
- `nb_day1_load_lakehouse_tables`
- Default semantic model for the Warehouse
- `rpt_day1_order_status` or an equivalent simple report

Also confirm that:

- The Lakehouse contains the three uploaded CSV files
- The Lakehouse tables were created successfully
- The Warehouse tables were created and loaded successfully
- The validation query results match `EXPECTED_RESULTS.md`
- The pipeline has at least one successful run

## 17. Files to Share with Learners

Share or point learners to these files:

- `02-LEARNER-LAB-GUIDE.md`
- `support-files/templates/learner-worksheet.md`
- `support-files/templates/evidence-log-template.csv`
- `support-files/sql/03_validation_queries.sql`
- `support-files/scenario/EXPECTED_RESULTS.md`

## 18. Troubleshooting Notes

- If the Lakehouse tables do not appear after the notebook runs, reopen the Lakehouse and refresh the page.
- If the Warehouse queries fail, rerun `01_create_warehouse_tables.sql` and then rerun `02_load_demo_data.sql`.
- If the report creation experience differs in your tenant, use any basic report-authoring option available from the Warehouse semantic layer.
- If permissions are limited, the learner can still complete the lab as an observation-based exercise.
