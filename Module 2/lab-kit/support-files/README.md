# Support Files

This folder contains all support files needed for the Day 2 lab.

## Folder Map

- `data/`: raw and incremental CSV data
- `notebooks/`: notebook code used to build Bronze, Silver, and Gold outputs
- `sql/`: validation queries
- `scenario/`: scenario context, data dictionary, known issues, and expected results
- `templates/`: learner worksheet and evidence log template

## How These Files Are Used

- Upload the CSV files from `data/` into the Lakehouse
- Paste the notebook scripts from `notebooks/` into Fabric notebooks attached to the Lakehouse
- Run the SQL queries from `sql/` in the Lakehouse SQL analytics endpoint
- Use the documents in `scenario/` to explain the quality issues and expected outcomes
- Use the templates in `templates/` as learner handouts
