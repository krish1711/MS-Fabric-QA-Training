# Demo Scenario

## Scenario Name

Contoso Outdoor Retail Lakehouse and Warehouse Validation

## Scenario Summary

This Day 3 lab uses a small Fabric scenario in which the same business data is represented in both a Lakehouse and a Warehouse.

The goal of the scenario is to help QA learners practice:

- Delta-table validation
- Delta history inspection
- Warehouse SQL validation
- CTAS validation
- MERGE validation
- cross-surface reconciliation

## Demo Story

The raw customer, product, and order files are first loaded into a Lakehouse, where Delta tables are created.

Then:

- a controlled update and insert are applied to the Lakehouse orders table to create new history
- the same base business data is loaded into a Warehouse
- a CTAS table is created from the Warehouse data
- a MERGE script applies the same update and insert pattern to the Warehouse

Learners will validate the state of each surface and confirm that the final Lakehouse and Warehouse results match.
