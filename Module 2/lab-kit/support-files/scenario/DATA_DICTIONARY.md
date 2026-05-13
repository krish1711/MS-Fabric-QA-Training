# Data Dictionary

## customers_raw.csv

| Column | Description |
| --- | --- |
| `CustomerID` | Customer identifier |
| `CustomerName` | Customer display name |
| `Region` | Customer sales region |
| `CustomerType` | Enterprise or SMB |
| `IsActive` | `Y` or `N` active flag |

## products_raw.csv

| Column | Description |
| --- | --- |
| `ProductID` | Product identifier |
| `ProductName` | Product display name |
| `Category` | Product category |
| `StandardPrice` | Standard unit price |

## orders_full_raw.csv

| Column | Description |
| --- | --- |
| `OrderID` | Sales order identifier |
| `OrderDate` | Order date |
| `CustomerID` | Customer identifier |
| `ProductID` | Product identifier |
| `Quantity` | Ordered quantity |
| `UnitPrice` | Unit price used on the order |
| `OrderAmount` | Total order amount |
| `OrderStatus` | Business order status |

## orders_incremental_raw.csv

| Column | Description |
| --- | --- |
| `OrderID` | Sales order identifier |
| `OrderDate` | Order date |
| `CustomerID` | Customer identifier |
| `ProductID` | Product identifier |
| `Quantity` | Ordered quantity |
| `UnitPrice` | Unit price used on the order |
| `OrderAmount` | Total order amount |
| `OrderStatus` | Business order status |

## Tables Created in the Lakehouse

- `bronze_customers`
- `bronze_products`
- `bronze_orders`
- `silver_customers`
- `silver_products`
- `silver_orders`
- `silver_order_rejections`
- `gold_region_sales_summary`
