# Monitoring Checklist

Use this checklist when reviewing Monitoring Hub or pipeline run history.

## Capture these fields for the failed run

- pipeline name
- run status
- start time
- end time
- duration
- activity statuses
- failure message from the threshold step

## Capture these fields for the successful rerun

- pipeline name
- run status
- start time
- end time
- duration
- activity statuses

## Compare these runtime observations

- fast activity duration versus slow activity duration
- failed run versus successful rerun
- which activities completed before the failure occurred

## QA conclusion prompts

- which duration difference is large enough to document?
- does the failure message provide enough actionability?
- would this runtime pattern block release readiness?
