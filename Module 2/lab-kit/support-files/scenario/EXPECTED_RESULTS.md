# Expected Results

Use this file to validate that the demo environment was loaded and transformed correctly.

## Full Load Expected Counts

### Bronze counts

- `bronze_customers`: `6`
- `bronze_products`: `6`
- `bronze_orders`: `8`

### Silver counts

- `silver_customers`: `5`
- `silver_products`: `5`
- `silver_orders`: `3`
- `silver_order_rejections`: `5`

### Gold row count

- `gold_region_sales_summary`: `3`

## Full Load Expected Gold Summary

| Region | OrderCount | TotalOrderAmount |
| --- | --- | --- |
| `East` | `1` | `980.00` |
| `North` | `1` | `2400.00` |
| `West` | `1` | `300.00` |

## Incremental Load Expected Results

### Accepted incremental rows

- `1`

### Rejected incremental rows

- `2`

### Silver order count after incremental load

- `4`

### Silver rejection count after incremental load

- `7`

## Gold Summary After Incremental Load

| Region | OrderCount | TotalOrderAmount |
| --- | --- | --- |
| `East` | `1` | `980.00` |
| `North` | `2` | `3500.00` |
| `West` | `1` | `300.00` |
