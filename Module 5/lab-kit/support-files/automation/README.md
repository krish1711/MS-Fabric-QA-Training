# Day 5 Automation Files

This folder contains a small pytest-based validation suite for the Day 5 lab.

## What these files do

The tests do not call Fabric directly. Instead, they validate an `observed_results.json` file that you populate with the results you observed in Fabric.

This keeps the first automation example simple and teaches a useful idea:

- capture stable observations
- structure them clearly
- validate them automatically

## Files

- `requirements.txt`: installs `pytest`
- `observed_results.template.json`: blank template for learner use
- `sample_observed_results.json`: sample file that matches the expected Day 5 results
- `tests/test_day5_results.py`: pytest checks for statuses, counts, totals, and duration comparison

## Setup

1. Copy `observed_results.template.json` to `observed_results.json`.
2. Replace the placeholder values with the results you observed in Fabric.
3. Install dependencies if needed:

```bash
python3 -m pip install -r requirements.txt
```

4. Run the tests:

```bash
python3 -m pytest tests/test_day5_results.py
```

## Optional sample run

If you want to verify the suite with the packaged sample file first, run:

```bash
OBSERVED_RESULTS_PATH=sample_observed_results.json python3 -m pytest tests/test_day5_results.py
```
