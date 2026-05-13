# Day 2 Lab Kit

This folder contains the complete lab package for **Module 2: Data Validation & Quality Testing**.

## Use This Folder In This Order

1. `01-INSTRUCTOR-SETUP.md`
2. `02-LEARNER-LAB-GUIDE.md`
3. `support-files/`

## What This Lab Kit Includes

- A step-by-step instructor setup guide
- A full end-to-end learner lab guide written in an exercise-and-task format
- Raw CSV support data with intentional quality issues
- An incremental order file for late-arriving and incorrect data scenarios
- Notebook scripts for Bronze, Silver/Gold, and incremental processing
- SQL validation queries
- A learner worksheet and evidence log template
- Scenario, data dictionary, issue summary, and expected results documents

## Recommended Demo Asset Names

Use these names unless your environment already has a preferred naming standard:

- Workspace: `ws_day2_contoso_quality`
- Lakehouse: `lh_day2_contoso_quality`
- Notebook 1: `nb_day2_bronze_load`
- Notebook 2: `nb_day2_silver_gold_build`
- Notebook 3: `nb_day2_incremental_load`

## Lab Objective

By the end of the lab, learners should be able to:

- build a simple medallion-style Fabric environment
- identify quality defects in Bronze data
- validate cleansing logic in Silver
- validate business-ready outputs in Gold
- compare full-load and incremental-load results
- record QA evidence and test-case thinking

## Folder Structure

- `support-files/data/`: raw and incremental CSV files
- `support-files/notebooks/`: notebook code used in the lab
- `support-files/sql/`: validation queries for Lakehouse SQL endpoint
- `support-files/scenario/`: scenario, data dictionary, issues, and expected results
- `support-files/templates/`: worksheet and evidence log templates
