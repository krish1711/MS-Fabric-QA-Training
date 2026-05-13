# Support Files

This folder contains all support files needed for the Day 3 lab.

## Folder Map

- `data/`: base and update CSV files
- `notebooks/`: notebook code used to build and update Lakehouse Delta tables
- `sql/`: Warehouse setup, CTAS, MERGE, and validation scripts
- `scenario/`: scenario context, data dictionary, change scenario, and expected results
- `templates/`: learner worksheet and evidence log template

## How These Files Are Used

- Upload the CSV files from `data/` into the Lakehouse
- Paste the notebook scripts from `notebooks/` into Fabric notebooks attached to the Lakehouse
- Run the Warehouse SQL scripts from `sql/` in the Fabric Warehouse query editor
- Use the documents in `scenario/` to explain the expected Lakehouse and Warehouse behaviors
- Use the templates in `templates/` as learner handouts
