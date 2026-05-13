# Demo Scenario

## Scenario Name

Contoso Outdoor Retail Data Quality Flow

## Scenario Summary

This Day 2 lab uses a small Microsoft Fabric quality-testing scenario for **Contoso Outdoor Retail**.

The goal of the scenario is to help QA learners practice:

- medallion-layer validation
- structural quality checks
- business-rule checks
- full-load and incremental-load reasoning
- issue evidence collection

## Demo Story

The raw input data contains intentional quality problems, including:

- missing values
- duplicate business keys
- invalid status values
- invalid customer references
- duplicate replay behavior in the incremental load

Learners will:

- load the raw files into Bronze
- inspect visible issues in Bronze
- apply cleansing and validation logic in Silver
- inspect trusted summary outputs in Gold
- apply an incremental file and validate how accepted and rejected records behave

## Why This Scenario Works for Day 2

The dataset is small enough to inspect manually, but rich enough to demonstrate:

- the difference between structural and business-rule defects
- the difference between Bronze, Silver, and Gold expectations
- the extra complexity introduced by incremental processing
