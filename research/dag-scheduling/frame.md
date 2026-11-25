# Frame: exact or learned scheduling for delegating jobs to agents

The hub must assign jobs, each a task with a class, to AI agents that differ in cost and reliability, as a DAG of tasks over rounds, and solves it exactly today.

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md)

## The problem in one sentence

Which agent should run which task, in which round, when each agent's chance of passing is only estimated, so that the DAG finishes at the least cost per passed job.

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| Problem | **scheduling on unrelated machines**: each machine has its own time per job | (Lenstra 1990, title) |
| Problem | **the generalized assignment problem**: jobs to machines under cost and capacity | (Shmoys 1993, title) |
| Method | **min-cost flow**: the assignment bought as a flow of least cost | the hub's planner |
| Setting | **stochastic scheduling**: durations or success drawn from distributions not fully known | (Allahverdi 2022, abstract) |
| Method | **algorithms with predictions**, also called learning-augmented: advice used without a distribution | (Mitzenmacher 2022, title) |
| Practice | **model routing** and **cascades**: each call sent to the cheapest model that can pass it | (Moslem 2026, abstract) |

## What practice calls it

- Delegating, in this hub: a ladder of rungs and a cascade that climbs it on failure.
- Orchestration, in the frameworks: a graph of nodes over shared state (LangChain 2026, overview).
- Routing, at the vendors: easy queries to a small model, hard ones up a tier (Anthropic 2024, the routing section).

## Does the repository's name match?

- The folder says dag-scheduling, the field's word for tasks with precedence on machines; the practice word delegating names who decides, not what is solved.
- Both names are true; the field's is the better search handle, and this review keeps the folder's name.

## Sub-questions

| Question | Strand in review.md |
|---|---|
| Q1 exact assignment and scheduling under uncertain durations and success | Strand 1 |
| Q2 learned schedulers against exact ones at equal budget, and guarantees for advice | Strand 2 |
| Q3 routing, cascades and orchestration of model calls in practice | Strand 3 |
| Q4 estimating an agent's per-class pass rate from few observations | Strand 4 |

## Held elsewhere

- Why one agent beats another on a class, the specialisation rule, is the lab's review (Tewf-lab 2026 specialisation).
- The estimators, pass rates predicted from tests, are the lab's other review (Tewf-lab 2026 estimators).
