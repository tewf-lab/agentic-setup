# Baseline: the comparator, named

B1 is the framework the hub most resembles in loop and least resembles in enforcement, and with it this review closes.

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)

## B1: Kambhampati 2024, the LLM-Modulo framework

1. A position paper published at ICML 2024 argues that autoregressive models cannot plan or self-verify, and should propose while external sound verifiers check (Kambhampati 2024, abstract).
2. Its technical companion runs the loop: verifiers validate, the model is re-prompted on failure, and outputs stay inside what verifiers accept (Gundawar 2024, abstract; secondary).
3. It is the baseline here because the hub runs the same loop with different critics: acceptance tests, a path guard and a judging seat.

## Compared piece by piece

| Item | In B1 | The hub |
|---|---|---|
| proposer | one model in a loop | a worker model on the cheapest allowed rung |
| critics | external, sound, model-based | acceptance tests, a path guard, a judging seat |
| on failure | re-prompt with the critique | climb one rung and retry fresh |
| mediator | none named | a hook before every tool call, denying by default |
| economy | not modelled | ceilings, never-lists, a share cap, a cap per job |
| record | none required | one ledger row per attempt |
| guarantee | sound if the critics are | tests pass and scope kept, no soundness claim |

## What B1 lacks

- Any mediation of tool calls; its loop governs outputs, not the acts of acting (Strand 1 of [review](review.md)).
- A cost policy; the cascade literature beside it pays for the rungs (Strand 3 of [review](review.md)).
- Isolation of a run, and a ledger to be measured on.

## How the comparison is measured

- Both run over the same ledger of jobs, and the measure is cost per passed job, the hub's own metric.
- Scope violations count as failures, not trades; the share cap and the per-job cap stay as the hub enforces them.
- The guarantee differs in kind: B1's is logical and the hub's is empirical, so the ledger is the arbiter.

## The review is finished

- B1 is named: Kambhampati 2024, its propose-and-verify loop against the hub's gated ladder, on cost per passed job.
