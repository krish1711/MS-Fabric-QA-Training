# Change Scenario

The Day 3 change scenario is intentionally simple so learners can validate the exact before-and-after behavior.

## Base State

The base order data contains six orders.

## Change 1: Update an existing order

- `OrderID`: `SO30003`
- Original status: `Processing`
- Updated status: `Shipped`
- Original amount: `180.00`
- Updated amount: `225.00`

## Change 2: Insert a new order

- `OrderID`: `SO30007`
- New amount: `90.00`
- Region: `North`

## Why This Matters for QA

This controlled change scenario allows learners to validate:

- Delta history visibility in the Lakehouse
- MERGE update and insert behavior in the Warehouse
- final aggregate reconciliation across both surfaces
