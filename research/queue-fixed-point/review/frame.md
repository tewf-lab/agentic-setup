# Frame: what the field calls a work queue driven to a fixed point

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md)

Step 1 of the review for [agentic-setup#1](https://github.com/tewf-lab/agentic-setup/issues/1), read on 2026-11-25. It states the problem, gives the field's names beside the practitioners', and says whether the repository's name matches. The sources are in [sources](sources.md), the state of the art per strand in [state-of-the-art](state-of-the-art.md), the baseline in [baseline](baseline.md).

## The problem in one sentence

A steering session is told "finish everything open in the reference implementation and the lab", but the work it does comes from a list someone wrote into its prompt: which exact method makes the work done converge on the work asked, without anyone enumerating it?

Terms used below, defined once:

- A **source of open work** is a persistent register that holds work not yet done: the issues of the registered repositories, DAG tasks not done or stuck, the unmet "Done when" of briefs and prompts, a request not yet filed.
- A **queue** is a program's prioritized list, built by reading the sources, never from a prompt.
- A **worklist algorithm** takes an item, processes it, and re-queues whatever the processing changed, until nothing changes (Kildall 1973).
- A **fixed point** is a state a rebuild does not change: rebuilding the queue adds nothing the seat can act on (the field's form: an extremal fixpoint of a system of equations, Cousot & Cousot 1977).
- **Coverage** is items closed over items open at the start plus items created during the run.
- **Pre-RS traceability** is the link from a requirement back to its origin, before any specification exists (Gotel & Finkelstein 1994).
- A **closing keyword** is practice's mechanism by which done work closes its source: "Closes #10" in a pull request merged to the default branch (GitHub Docs 2026).
- **Decomposition as needed** is decomposing an item only when the seat reaches it, knowing the current state, as SHOP2 does for tasks (Nau et al. 2003).
- A **cap** is an iteration budget, the practitioner's substitute when no fixed point is reached (Manus 2025, for agent loops; the issue's "or the cap is reached").

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| the loop itself | **worklist algorithm**, iterative data-flow analysis | Kildall 1973 |
| iterating a set of equations in a chosen order | **chaotic iteration** over a dependency graph | Stiévenart et al. 2021 |
| the stop state | **fixed point**, the extremal fixpoint of a monotone system | Cousot & Cousot 1977 |
| why it stops | order-preserving functions, finite iteration; approximation when chains are infinite | Kildall 1973; Cousot & Cousot 1977 |
| the link request → issue → change → test | **requirements traceability**, pre-RS and post-RS | Gotel & Finkelstein 1994 |
| the model of which links to keep | **reference model**, low-end vs high-end traceability | Ramesh & Jarke 2001 |
| how done work closes its source (practice) | **closing keyword**, linked pull request | GitHub Docs 2026 |
| the measure of a worked set | **test adequacy criterion** as a **stopping rule**; coverage ratio | Zhu, Hall & May 1997 |
| an agent's score on real work items | **resolved rate** | Jimenez et al. 2024 |
| the loop of a coding agent | **agent loop**: action, observation, next iteration, until the task is complete | Yang et al. 2024; Manus 2025 |
| the model shaping its own context | **context engineering** | Cognition 2025; Manus 2025 |
| breaking a task too big for one step | **HTN planning**, method, compound task | Erol, Hendler & Nau 1994 |
| decomposition ordered by execution | decomposition **in execution order**, as needed | Nau et al. 2003 |
| an LLM decomposing its own work | **decomposed prompting**, **least-to-most prompting** | Khot et al. 2023; Zhou et al. 2023 |

## What practice calls it

- **Task queue** and **task management agent**: BabyAGI, "an AI-powered task management system... creates tasks based on the result of previous tasks" (BabyAGI 2023).
- **Backlog**, **velocity**, **known and unknown work**: the product owner's list and the team's rate of closing it, forecast as a range (Mountain Goat 2026).
- **Night prompt**, **session**, **seat**: the reference implementation's own practice, the hand-written list this review is to replace.
- **Closing the loop**: "Closes #10" in a pull request; the merge closes the issue (GitHub Docs 2026).
- **Agent**, **subagent**, **workflow**: the frameworks' words, with the agent's completion decided inside the loop (Anthropic 2024; Cognition 2025).

## Does the repository's name match?

- Yes, unusually well. The work item **queue-fixed-point** and the issue's "a queue built by a program, worked to a fixed point" use the field's own words: the **worklist** (Kildall 1973) and the **fixed point** (Cousot & Cousot 1977). No renaming is proposed.
- The risk is the analogy, not the name. The field's termination results hold for order-preserving iteration over a fixed set of equations; a backlog is neither fixed nor a lattice, and that gap is carried into [state-of-the-art](state-of-the-art.md) as the limit of strand 1.

## In and out

In: the five strands below, for one seat working a program-built queue, closing sources as items finish, stopping at a fixed point or a cap, measured by coverage.
Out: multi-agent coordination, delegation and incentives (held elsewhere); scheduling and priority theory beyond the queue's order; the cost model of a night's tokens; the reference implementation itself (the pin, after the design).

## Sub-questions

| Question | Strand |
|---|---|
| Q1 Does a worklist iterated over open work converge, and what makes it terminate? | Strand 1 |
| Q2 How does work trace back to a request, and how does done work close its source? | Strand 2 |
| Q3 How is coverage of a backlog measured, including items created while working it? | Strand 3 |
| Q4 How do long-running agent loops decide they are done? | Strand 4 |
| Q5 How is an item too big for one job decomposed, and when? | Strand 5 |

## Held elsewhere

- The question, the case of 25 Nov 2026 and the tests the method must pass: [agentic-setup#1](https://github.com/tewf-lab/agentic-setup/issues/1).
- Multi-agent teams, delegation and incentives: the [multi-agent-teams](https://github.com/Tewf/ai-augmented-agents/blob/8a05e7eb88a41cfb53c8188fc9faacac94e79d02/evidence/multi-agent-teams/README.md) review, in the agents repository.
- The seat and the delegator that would work the queue: `maestro/delegator.py`, out of scope for a review.
