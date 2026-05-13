# Data Dictionary

## customers.csv

- `CustomerID`: unique customer identifier
- `CustomerName`: customer display name
- `Region`: region used for reporting and grouping
- `CustomerSegment`: business segment such as `Enterprise` or `SMB`
- `IsActive`: active status flag

## products.csv

- `ProductID`: unique product identifier
- `ProductName`: product display name
- `Category`: product category used for reporting
- `UnitPrice`: standard unit price
- `IsActive`: active status flag

## orders.csv

- `OrderID`: unique sales order identifier
- `OrderDate`: order date
- `CustomerID`: customer key
- `ProductID`: product key
- `Quantity`: number of units sold
- `UnitPrice`: unit price at sale time
- `OrderAmount`: total order amount
- `OrderStatus`: order completion status
