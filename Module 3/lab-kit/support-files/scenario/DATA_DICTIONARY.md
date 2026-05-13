# Data Dictionary

## customers.csv

| Column | Description |
| --- | --- |
| `CustomerID` | Customer identifier |
| `CustomerName` | Customer display name |
| `Region` | Customer region |
| `CustomerType` | Enterprise or SMB |
| `IsActive` | `Y` or `N` active flag |

## products.csv

| Column | Description |
| --- | --- |
| `ProductID` | Product identifier |
| `ProductName` | Product display name |
| `Category` | Product category |
| `StandardPrice` | Standard unit price |

## orders_base.csv

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

## order_updates.csv

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
| `OperationType` | `UPDATE` or `INSERT` |
