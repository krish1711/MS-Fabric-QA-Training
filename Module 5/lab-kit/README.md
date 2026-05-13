# Day 5 Lab Kit

This folder contains the complete lab package for **Module 5: Performance, Monitoring & Test Automation Fundamentals**.

## Use This Folder In This Order

1. `01-INSTRUCTOR-SETUP.md`
2. `02-LEARNER-LAB-GUIDE.md`
3. `support-files/`

## What This Lab Kit Includes

- a step-by-step instructor setup guide
- a full end-to-end learner lab guide written in an exercise-and-task format
- CSV support data for the Day 5 monitoring scenario
- notebook scripts for fast, slow, fail, and pass validation activities
- SQL scripts for Warehouse setup and validation
- monitoring and automation guidance files
- a small pytest automation suite and observed-results templates
- a learner worksheet and evidence log template

## Recommended Demo Asset Names

Use these names unless your environment already has a preferred naming standard:

- Workspace: `ws_day5_contoso_monitoring`
- Lakehouse: `lh_day5_contoso_runtime`
- Warehouse: `wh_day5_contoso_reporting`
- Notebook 1: `nb_day5_build_perf_tables`
- Notebook 2: `nb_day5_fast_metric_check`
- Notebook 3: `nb_day5_slow_metric_check`
- Notebook 4: `nb_day5_threshold_fail`
- Notebook 5: `nb_day5_threshold_pass`
- Pipeline: `pl_day5_contoso_monitoring`

## Lab Objective

By the end of the lab, learners should be able to:

- compare activity durations in a Fabric pipeline
- inspect run history and Monitoring Hub evidence
- recognize a deliberate failure pattern
- validate reporting totals with SQL
- run a first-pass pytest suite against observed results
- classify manual checks versus automation candidates

## Folder Structure

- `support-files/data/`: CSV files to upload to the Lakehouse
- `support-files/notebooks/`: notebook code used in the pipeline
- `support-files/sql/`: Warehouse setup and validation scripts
- `support-files/scenario/`: scenario, expected results, monitoring checklist, and automation boundaries
- `support-files/automation/`: pytest files, templates, and automation instructions
- `support-files/templates/`: worksheet and evidence log templates
