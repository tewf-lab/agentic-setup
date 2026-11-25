# agentic-setup

The standard of an agentic setup: eleven practices, the research behind them, and the checker that holds an implementation to them.

> Status: version 0.1.0 in preparation, 2026-11-25.

**Shape:** [folder](https://github.com/Tewf/reader-ergonomics/blob/master/shapes/readme-and-folder.md)

## What it is

This repository is the concept of an agentic setup, not an implementation of one. It holds three parts:

- `standard.toml`: the standard: eleven practices, each with what it requires and the source it comes from.
- `research/`: the studies behind the practices, from reviews of the field to measurements of the workflow itself.
- `checks/instance.py`: the instance checker, which holds an implementation to the standard.

An implementation is its own repository, with its own agents, its own tests and its own ledger; this repository says what any implementation must hold, and checks that it holds it. The first implementation is the reference implementation.

## The standard

`standard.toml` is the source of truth; this table restates it.

| id | name | what it requires |
| ---- | ---- | ---- |
| S1 | gate | a reference monitor runs before every tool call of the steering model, denies by default and fails closed |
| S2 | delegation | the steering model does not author the bulk: an exact method assigns each task to an agent from a matrix of agents and estimators fed by the oracles |
| S3 | acceptance | every task's result is judged by a test a program runs, never by the model that did the work |
| S4 | scope | a task's changes are held to the scope it declared |
| S5 | ledger | every attempt is recorded with its agent, its outcome and its cost |
| S6 | dag | the work is held as a graph of tasks: every open issue is one, none is stuck, and a program, not the steering model, starts each ready task that carries a check |
| S7 | cap | the steering model's own usage is measured against a cap that stops it |
| S8 | task-template | every task is made from the template and checked against the families its kind names |
| S9 | push | every task ends pushed, and the server's CI checks it again |
| S10 | roles | every kind of task names the roles that cover it (skills as the heuristic, tools, exact methods), and a program checks they are present before the work starts |
| S11 | improvement | the outcome of every task feeds the estimators and a gap detector, and a gap opens a task that creates or improves a role, a tool or the workflow |

How the practices chain into one workflow, each step with its test: [workflow.md](workflow.md). Who plays each part: [organisation.md](organisation.md).

## How an implementation is checked

An instance maps each practice of the standard to the files that hold it and the test command that proves it, in its own `agentic-setup.toml`:

```toml
[S1]
files = ["gate.py"]
test = "python3 -m unittest test_gate.py"
```

From this repository, `python3 checks/instance.py --instance PATH` then checks the instance against `standard.toml`: it fails when a practice is unmapped, a mapped file is missing, or a test command fails, and it warns when a practice is waived with a reason. `python3 checks/instance.py --list` lists the practices. The reference implementation is checked this way.

## Research

- [research/architecture](research/architecture): the review the standard stands on: protection principles, guardrails over agent actions, and propose-and-verify with sound critics.
- [research/dag-scheduling](research/dag-scheduling): the assignment of tasks to agents under cost and capacity, and the cascades and routers that cut the cost of it.
- [research/workflow-performance](research/workflow-performance): the workflow itself, measured from the job ledger: where work passes, what a correct answer costs, what stops a job.
- [research/sandbox](research/sandbox): the review behind the scope practice: a task sandbox that holds a task's changes to the scope it declared.

## Scope

This repository holds the concept only: the standard, the research, the instance checker, and the checks that hold this repository to the family's shapes. It holds no implementation: an implementation is its own repository, checked from here. Generated research output under `research/*/out/` is outside the checks' scope. Nothing of one machine belongs here: no local path, and no name of a tool or model of one machine, because this repository may become public.
