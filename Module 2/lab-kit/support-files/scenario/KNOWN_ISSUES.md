# Known Issues in the Raw Data

Use this file to explain what learners should expect to find in the raw data.

## Customer Data Issues

- One customer record has a missing `Region`

## Product Data Issues

- One product record has a missing `Category`

## Full Order Data Issues

- One order has a missing `CustomerID`
- One order references a customer that does not exist in the customer file
- One order has an invalid `OrderStatus`
- One order duplicates an existing `OrderID`

## Incremental Order Data Issues

- One row is a valid late-arriving order and should be accepted
- One row is a duplicate replay of an already-loaded `OrderID`
- One row has an invalid status and should be rejected

## QA Interpretation

These issues are intentional. The goal is not to “fix the dataset” manually. The goal is to help learners practice:

- identifying quality defects in Bronze
- validating how Silver applies acceptance and rejection logic
- confirming that Gold only includes trusted records
