# Day 3 Lab Kit

This folder contains the complete lab package for **Module 3: Lakehouse & Warehouse Testing**.

## Use This Folder In This Order

1. `01-INSTRUCTOR-SETUP.md`
2. `02-LEARNER-LAB-GUIDE.md`
3. `support-files/`

## What This Lab Kit Includes

- A step-by-step instructor setup guide
- A full end-to-end learner lab guide written in an exercise-and-task format
- CSV support data for Lakehouse and Warehouse setup
- Notebook scripts for Lakehouse Delta-table creation and Lakehouse updates
- SQL scripts for Warehouse table creation, base loading, CTAS, MERGE, and validation
- A learner worksheet and evidence log template
- Scenario, data dictionary, change scenario, and expected results documents

## Recommended Demo Asset Names

Use these names unless your environment already has a preferred naming standard:

- Workspace: `ws_day3_contoso_lh_wh`
- Lakehouse: `lh_day3_contoso`
- Warehouse: `wh_day3_contoso`
- Notebook 1: `nb_day3_build_lakehouse_tables`
- Notebook 2: `nb_day3_apply_lakehouse_update`

## Lab Objective

By the end of the lab, learners should be able to:

- create and inspect Delta-backed Lakehouse tables
- use Delta history as QA evidence
- create and validate Warehouse tables with SQL
- validate CTAS output tables
- validate MERGE update and insert behavior
- reconcile Lakehouse and Warehouse outputs

## Folder Structure

- `support-files/data/`: CSV files to upload to the Lakehouse
- `support-files/notebooks/`: notebook code used in the lab
- `support-files/sql/`: Warehouse setup, CTAS, MERGE, and validation scripts
- `support-files/scenario/`: scenario, data dictionary, change scenario, and expected results
- `support-files/templates/`: worksheet and evidence log templates
