# Frame: the architecture this hub applies to its agents

The hub wraps its agents in a steering seat, a gate, a delegating ladder, isolated worktrees and a ledger, and each piece has an older name in the field.

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md)

## The problem in one sentence

How do you let models edit a real repository, at a bounded cost, when a rule given in prose does not hold and a wrong edit is expensive?

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| Principle | **complete mediation** and **least privilege**: every access checked, no more right than needed | (Saltzer 1975, the paper's principles) |
| Mechanism | **the reference monitor**: a small, always-invoked, tamper-resistant mediator of access | (Abbott 1976, a report of that line) |
| Defence | **the instruction hierarchy**: a model trained to obey operator text over outside text | (Wallace 2024, title) |
| Defence | **guardrails**: classifiers and rules that screen an agent's actions before they run | (Xiang 2024, title) |
| Pattern | **orchestrator-workers** with an **evaluator**: one seat divides the work and judges results | (Anthropic 2024, the patterns section) |
| Framework | **LLM-Modulo**: a model proposes, sound external verifiers check, the loop repeats | (Kambhampati 2024, title) |
| Economy | **the model cascade**: each call sent to the cheapest model that can still pass | (Chen 2023, title) |
| Oracle | **tests as acceptance**: an issue counts resolved when the repository's own tests pass | (Jimenez 2024, title) |

## What practice calls it

- The seat, in this hub: a steering role that reads, judges and dispatches, barred from authoring anything.
- The gate: a hook that runs before every tool call and denies whatever its list does not name.
- The ladder: job classes with ceilings and never-lists, climbing one rung when the judge says the answer failed.
- The envelope: a small report back, with the diff read only when something looks wrong.

## Does the repository's name match?

- The folder says architecture, and the field says agent architecture for exactly this bundle of seat, tools and control.
- The pieces carry older names than the bundle, so this review searches the pieces and not the bundle.

## Sub-questions

| Question | Strand in review.md |
|---|---|
| Q1 security and control: reference monitors, complete mediation, least privilege, guardrails, a prompt rule against an enforced hook | Strand 1 |
| Q2 orchestration: orchestrator-worker patterns, LLM-Modulo, tests as the oracle of generated code | Strand 2 |
| Q3 cost: model cascades and routing, and budgets enforced per job | Strand 3 |
| Q4 practice, as grey literature: the guidance of framework makers and laboratories | Strand 4 |

## Held elsewhere

- Which rung should run which task, as an optimisation, is [the sibling study](../dag-scheduling/frame.md).
- The measured cost history of the workflow is the workflow-performance study of this folder.
