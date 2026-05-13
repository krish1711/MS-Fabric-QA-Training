# Measures, Relationships, and Roles

Use this file when shaping the default semantic model for the Day 4 lab.

## Relationships

Create these relationships:

1. `FactSales[CustomerID]` to `DimCustomer[CustomerID]`
2. `FactSales[ProductID]` to `DimProduct[ProductID]`

Use these settings for both:

- cardinality: many-to-one
- cross-filter direction: single
- active relationship: yes

## Measures

Create these measures in the `FactSales` table.

### `Total Sales`

```DAX
Total Sales = SUM(FactSales[OrderAmount])
```

### `Order Count`

```DAX
Order Count = COUNTROWS(FactSales)
```

### `Average Order Value`

```DAX
Average Order Value = DIVIDE([Total Sales], [Order Count])
```

## RLS roles

Create these roles on the `DimCustomer` table.

### `NorthRole`

```DAX
[Region] = "North"
```

### `WestRole`

```DAX
[Region] = "West"
```

## QA notes

- the measures should match the SQL validation queries exactly
- if the report totals do not match SQL, recheck the relationships first
- if `View as` shows blank or incomplete results, confirm the role filters were added to `DimCustomer`, not `FactSales`
