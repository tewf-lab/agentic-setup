# Baseline: the hand-listed night prompt

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)

Step 5 of the review, the last. Evidence is in [sources](sources.md), the state of the art per strand in [state-of-the-art](state-of-the-art.md).

**Baseline:** B1, the hand-listed night prompt — a person enumerates the session's tasks in the prompt; measured by coverage, items closed over items open at the start plus items created during the run.

## B1: the hand-listed night prompt

1. A person reads the session, remembers what was asked, and writes the night prompt as a list of tasks: the queue is the prompt.
2. The seat works the list top to bottom; whatever is not listed is not worked, and when the run finds new work it is done only if the seat chooses to.
3. When the list runs out the run ends; new work found mid-run goes into the next prompt, patched in by hand.
4. Nothing measures the run: no count of what was open, what was created, what was closed.

The case that named this baseline is the night of 25 Nov 2026 in [agentic-setup#1](https://github.com/tewf-lab/agentic-setup/issues/1): the prompt listed three tasks, the seat worked them, and two more were added to the list after the run — the enumeration, not the work, was the bottleneck.

## Compared with what the review found

| Item | In B1 | Fit |
|---|---|---|
| Where the queue comes from (pre-RS traceability, Gotel & Finkelstein 1994) | a person writes it from memory of the session | lacks |
| The stopping rule (worklist to a fixed point, Kildall 1973; Cousot & Cousot 1977) | the run stops when the prompt's list ends | lacks |
| Closing the source of each item (closing keyword, GitHub Docs 2026) | done by hand, if the seat remembers | lacks |
| The measure (coverage as a stopping rule, Zhu, Hall & May 1997; resolved rate, Jimenez et al. 2024) | nothing is counted | lacks |
| Decomposition of an oversized item (decomposition as needed, Nau et al. 2003) | the seat decides, informally, mid-run | partial |
| One seat working a list, linearly (Cognition 2025) | one seat, top to bottom | matches |

## What B1 lacks

- A queue built from the sources of open work. The prompt's list is a pre-RS link written after the fact, and pre-RS links captured after the fact are recovered poorly (Gotel & Finkelstein 1994) — which is why tasks had to be added after the 25 Nov 2026 run.
- A stopping rule that holds when work creates work. B1 stops on the list, not on the work; no fixed point is defined, let alone reached (Kildall 1973; the limit of strand 1, where no source proves termination for a set that grows).
- Automatic closing. The issue, the DAG task and the brief's "Done when" stay open until someone types the closing keyword by hand (GitHub Docs 2026).
- A measure. Nothing computes coverage, so B1 cannot be shown to be worth anything against a program-built queue (Zhu, Hall & May 1997).
- Decomposition when an item is too big for one job. Oversized items are worked whole or stall, where SHOP2 would decompose them at the moment it reaches them, knowing the current state (Nau et al. 2003).

## How it is measured

- Coverage = items closed / (items open at the start + items created during the run), counted over every registered source of open work: the issues, the DAG tasks, the briefs' "Done when", the requests not yet filed.
- Why it is the right one. An item never enumerated is never closed, so missing work shows in the numerator — the pre-RS gap made visible rather than patched after the run (Gotel & Finkelstein 1994). Runaway creation shows in the denominator — the cost of the cap made visible, the way unknown work is budgeted in practice (Mountain Goat 2026). It is a computable stopping rule in the adequacy-criterion sense (Zhu, Hall & May 1997), and it extends the resolved rate from a fixed set of real issues (Jimenez et al. 2024) to a live set that grows while it is worked.
- A run beats B1 when it holds a higher coverage over the same sources' items at the same morning checkpoint, and a program can recompute the count from the registers each morning, so the comparison is repeatable.

## The review is finished

The baseline is named: B1.
