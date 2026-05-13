# Day 4 Lab Kit

This folder contains the complete lab package for **Module 4: Pipeline, Semantic Model & Security Testing**.

## Use This Folder In This Order

1. `01-INSTRUCTOR-SETUP.md`
2. `02-LEARNER-LAB-GUIDE.md`
3. `support-files/`

## What This Lab Kit Includes

- a step-by-step instructor setup guide
- a full end-to-end learner lab guide written in an exercise-and-task format
- CSV support data for pipeline and reporting setup
- notebook scripts for curated-table creation and controlled checkpoint behavior
- SQL scripts for Warehouse setup and validation
- semantic model instructions for measures, relationships, and RLS
- a learner worksheet and evidence log template
- scenario, data dictionary, test matrix, and expected results documents

## Recommended Demo Asset Names

Use these names unless your environment already has a preferred naming standard:

- Workspace: `ws_day4_contoso_pipeline_security`
- Lakehouse: `lh_day4_contoso_ops`
- Warehouse: `wh_day4_contoso_reporting`
- Notebook 1: `nb_day4_build_curated_tables`
- Notebook 2: `nb_day4_qa_checkpoint_fail`
- Notebook 3: `nb_day4_qa_checkpoint_pass`
- Pipeline: `pl_day4_contoso_validation`

## Lab Objective

By the end of the lab, learners should be able to:

- create and run a Fabric pipeline
- inspect run history and failure details
- rerun a repaired pipeline successfully
- validate a Warehouse-backed semantic model
- create measures and a simple report
- test RLS roles with positive and negative outcomes

## Folder Structure

- `support-files/data/`: CSV files to upload to the Lakehouse
- `support-files/notebooks/`: notebook code used in the pipeline
- `support-files/sql/`: Warehouse setup and validation scripts
- `support-files/scenario/`: scenario, data dictionary, expected results, and test matrix
- `support-files/semantic-model/`: measures, relationship guidance, and RLS instructions
- `support-files/templates/`: worksheet and evidence log templates
