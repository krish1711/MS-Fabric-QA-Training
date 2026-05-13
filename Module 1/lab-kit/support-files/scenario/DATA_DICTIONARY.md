# Data Dictionary

## customers.csv

| Column | Description |
| --- | --- |
| `CustomerID` | Unique customer identifier |
| `CustomerName` | Customer display name |
| `Region` | Customer region |
| `CustomerType` | Enterprise or SMB |
| `IsActive` | `Y` when the customer is active |

## products.csv

| Column | Description |
| --- | --- |
| `ProductID` | Unique product identifier |
| `ProductName` | Product display name |
| `Category` | Product category |
| `StandardPrice` | Standard unit price |

## sales_orders.csv

| Column | Description |
| --- | --- |
| `OrderID` | Unique sales order identifier |
| `OrderDate` | Date of the order |
| `CustomerID` | Customer identifier |
| `ProductID` | Product identifier |
| `Quantity` | Units ordered |
| `UnitPrice` | Order unit price |
| `OrderAmount` | Quantity multiplied by UnitPrice |
| `OrderStatus` | Shipped, Processing, or Cancelled |

## Tables Created in the Lakehouse

- `customers`
- `products`
- `sales_orders`

## Tables Created in the Warehouse

- `dbo.Customers`
- `dbo.Products`
- `dbo.SalesOrders`
