# Day 5 Support Files

Use these support files with the Day 5 lab.

## Data

- `data/customers.csv`
- `data/products.csv`
- `data/orders.csv`

Upload these files to the Lakehouse folder `Files/day5-lab`.

## Notebooks

- `notebooks/01_build_perf_tables.py`
- `notebooks/02_fast_metric_check.py`
- `notebooks/03_slow_metric_check.py`
- `notebooks/04_threshold_fail.py`
- `notebooks/05_threshold_pass.py`

Use these notebooks to create the Day 5 pipeline and compare fast, slow, failed, and successful behavior.

## SQL

- `sql/01_create_warehouse_tables.sql`
- `sql/02_load_warehouse_data.sql`
- `sql/03_validation_queries.sql`

Use these scripts to create the reporting Warehouse, load the data, and validate the reporting outputs.

## Scenario and validation

- `scenario/SCENARIO.md`
- `scenario/DATA_DICTIONARY.md`
- `scenario/EXPECTED_RESULTS.md`
- `scenario/MONITORING_CHECKLIST.md`
- `scenario/AUTOMATION_BOUNDARIES.md`

These files define the business scenario, expected outputs, monitoring evidence, and automation guidance.

## Automation

- `automation/README.md`
- `automation/requirements.txt`
- `automation/observed_results.template.json`
- `automation/sample_observed_results.json`
- `automation/tests/test_day5_results.py`

Use these files to populate observed Fabric results and validate them with pytest.

## Templates

- `templates/learner-worksheet.md`
- `templates/evidence-log-template.csv`

Use these files to capture observations, evidence, and final conclusions.
