# Expected Results

Use this file to validate that the Day 4 environment was loaded and shaped correctly.

## Lakehouse Pipeline Output

- `stg_customers`: `6`
- `stg_products`: `5`
- `stg_orders`: `8`
- `qa_region_sales_summary`: `4`

## Overall Reporting KPIs

- `Total Sales`: `4680.00`
- `Order Count`: `8`
- `Average Order Value`: `585.00`

## Region Matrix Results

| Region | OrderCount | TotalSales |
| --- | --- | --- |
| `East` | `1` | `1500.00` |
| `North` | `3` | `1530.00` |
| `South` | `1` | `90.00` |
| `West` | `3` | `1560.00` |

## Restricted Role Results

### `NorthRole`

- visible order count: `3`
- visible total sales: `1530.00`
- visible regions: `North` only

### `WestRole`

- visible order count: `3`
- visible total sales: `1560.00`
- visible regions: `West` only

## Negative Security Expectations

- `NorthRole` must not show `East`, `South`, or `West` rows
- `WestRole` must not show `East`, `North`, or `South` rows
- unrestricted view should return to the full totals after **View as** is cleared
