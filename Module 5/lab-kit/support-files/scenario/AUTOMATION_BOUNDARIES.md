# Automation Boundaries

Use this file to decide what to automate first in the Day 5 scenario.

## Automate first

- row counts for core tables
- stable KPI totals
- expected regional aggregates
- pipeline status comparisons captured in structured form
- simple rules such as `slow activity duration > fast activity duration`

## Keep manual first

- subjective interpretation of whether a duration is acceptable for production
- monitoring-screen review that depends on UI layout or filtering choices
- capacity-pressure diagnosis that depends on environment-wide context
- exploratory troubleshooting after an unexpected failure

## Why this matters

The first automation suite should focus on stable, repeatable checks with a clear truth set. QA maturity comes from layering automation on top of good observations, not replacing judgment with brittle tests.
