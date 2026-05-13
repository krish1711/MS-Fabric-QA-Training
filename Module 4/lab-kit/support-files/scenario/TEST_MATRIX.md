# Day 4 Test Matrix

Use this matrix to keep the lab tied to QA outcomes.

## Pipeline execution

- confirm activity order is correct
- confirm first activity succeeds
- confirm checkpoint failure is visible in run history
- confirm the rerun completes after the checkpoint notebook is replaced

## Semantic model logic

- confirm customer and product relationships exist
- confirm relationships use the expected cardinality and filter direction
- confirm `Total Sales`, `Order Count`, and `Average Order Value` return expected values

## Report validation

- confirm KPI cards match expected totals
- confirm the region matrix matches expected totals
- confirm the report remains correct after refresh

## Security validation

- confirm `NorthRole` shows only North-region rows
- confirm `WestRole` shows only West-region rows
- confirm restricted roles block all other regions
- confirm unrestricted view returns to the full dataset
