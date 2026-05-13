# Demo Scenario

## Scenario Name

Contoso Outdoor Retail

## Scenario Summary

This Day 1 lab uses a small demo customer environment for a fictional retailer called **Contoso Outdoor Retail**.

The purpose of the scenario is not to teach deep data engineering. The purpose is to give QA learners a safe environment in which they can:

- navigate a Fabric workspace
- locate key Fabric items
- inspect both Lakehouse and Warehouse surfaces
- observe pipeline and semantic/report items
- think about customer-isolation boundaries

## Demo Story

Contoso Outdoor Retail uses Microsoft Fabric to store and analyze sales data for products, customers, and orders.

For Day 1, the workspace includes:

- one Lakehouse holding the uploaded source files and Delta tables
- one Warehouse holding relational copies of the same business data
- one Pipeline so learners can inspect a pipeline item and its run history
- one default semantic model
- one simple report

## Why This Scenario Works for Day 1

The dataset is intentionally small so learners can focus on:

- item discovery
- environment navigation
- QA evidence collection
- comparison of Lakehouse and Warehouse surfaces

## Recommended Demo Asset Names

- Workspace: `ws_day1_contoso_outdoor`
- Lakehouse: `lh_day1_contoso`
- Warehouse: `wh_day1_contoso`
- Pipeline: `pl_day1_navigation_demo`
- Notebook: `nb_day1_load_lakehouse_tables`
- Report: `rpt_day1_order_status`
