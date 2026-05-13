# Expected Results

Use this file to validate that the Day 5 environment was loaded and monitored correctly.

## Lakehouse Output

- `perf_customers`: `6`
- `perf_products`: `5`
- `perf_orders`: `10`
- `perf_region_sales_summary`: `4`

## Pipeline Run Expectations

- first pipeline run overall status: `Failed`
- second pipeline run overall status: `Succeeded`
- fast activity status: `Succeeded`
- slow activity status: `Succeeded`
- threshold activity first-run status: `Failed`
- threshold activity rerun status: `Succeeded`
- slow activity duration should be greater than fast activity duration

## Warehouse KPIs

- `Total Sales`: `5070.00`
- `Order Count`: `10`
- `Average Order Value`: `507.00`

## Region Totals

| Region | OrderCount | TotalSales |
| --- | --- | --- |
| `East` | `2` | `1590.00` |
| `North` | `3` | `1530.00` |
| `South` | `2` | `390.00` |
| `West` | `3` | `1560.00` |

## Automation Expectation

- the pytest suite should pass when the observed-results file contains the correct Fabric observations
