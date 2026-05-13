# Expected Results

Use this file to validate that the demo environment was loaded and transformed correctly.

## Base State Expected Counts

- `lake_customers`: `4`
- `lake_products`: `4`
- `lake_orders` before update: `6`
- `dbo.SalesOrders` before MERGE: `6`

## Base Regional Totals

| Region | OrderCount | TotalOrderAmount |
| --- | --- | --- |
| `East` | `1` | `1500.00` |
| `North` | `2` | `2574.00` |
| `South` | `1` | `180.00` |
| `West` | `2` | `570.00` |

## CTAS Expected Output

Table: `dbo.RegionSalesCTAS`

| Region | OrderCount | TotalOrderAmount |
| --- | --- | --- |
| `East` | `1` | `1500.00` |
| `North` | `2` | `2574.00` |
| `South` | `1` | `180.00` |
| `West` | `2` | `570.00` |

## Final State After Lakehouse Update and Warehouse MERGE

- final Lakehouse orders count: `7`
- final Warehouse `SalesOrders` count: `7`

## Final Regional Totals

| Region | OrderCount | TotalOrderAmount |
| --- | --- | --- |
| `East` | `1` | `1500.00` |
| `North` | `3` | `2664.00` |
| `South` | `1` | `225.00` |
| `West` | `2` | `570.00` |

## Delta History Expectation

After the Lakehouse update notebook runs, the `lake_orders` table should show at least:

- one initial write
- one update operation
- one additional write or insert-related operation
