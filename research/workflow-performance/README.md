# Workflow performance, read from the job ledger

This study measures the hub's own workflow from its job ledger — the JSON lines of `logs/cost_ledger.jsonl`, one row per attempt — to decide where jobs should go.

**Shape:** [project](https://github.com/Tewf/reader-ergonomics-project/blob/master/shapes/project.md)

## The question

When the delegator sends a job up its chain of rungs, cheapest first, where does the work actually pass? Which backend passes on the first attempt, which classes it fails, what a correct answer costs in tokens and dollars, how often the path guard or the plan's own quota stops a job rather than the agent failing it, and how long a job spans from its first row to its last.

## The data

The ledger the delegator itself appends to: one JSON line per attempt, with the keys `ts`, `job`, `attempt`, `repo`, `class`, `backend`, `tokens_in`, `tokens_out`, `cache_read`, `usd`, `oracle`, `path_guard`, `escalated_from`. A row counts as an attempt only when its oracle is `pass` or `fail`; rows that are `orphaned`, `spec_error` or `quota` are counted apart, never as attempts, and a row the path guard stopped is counted under guard violations.

## Rerun it

```
python3 research/workflow-performance/analyse.py logs/cost_ledger.jsonl
python3 research/workflow-performance/analyse.py logs/cost_ledger.jsonl --markdown
```

The first command prints the report as JSON, the second as markdown tables. Every figure is checked by
`python3 -m unittest discover -s research/workflow-performance -p test_*.py` against a fixture ledger written inside the test, never the real one.

## What it does not measure yet

- GLM credits per call: a glm row's `usd` is 0 by construction (a flat plan) and its `glm_credits` is null, derived rather than read, so what a glm pass really spends is not in the ledger.
- The steering seat's own tokens: the session that writes the specs, dispatches the jobs and reads the envelopes sits in no row of this ledger, so the cost of steering itself is not measured.
