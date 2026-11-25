# State of the art: the best known per strand

**Shape:** [state of the art](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/state-of-the-art.md)

Step 3 of the review. One section per question of the [frame](frame.md), in its order; the best evidence is kept apart from the practice most adopted, an upper bound from a limit. Sources are in [sources](sources.md); every holder is a key from that pool. The grades: proved, measured, survey, convention, not found.

## Q1 Does a worklist iterated over open work converge, and what makes it terminate?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Kildall 1973 | The general worklist — process a node, propagate to successors, intersect, re-queue on change — computes the solution of a system of monotone equations and halts, because the information only descends on a finite structure. | proved |
| Upper bound | Cousot & Cousot 1977 | Termination is always purchasable: when Kleene's iteration sequence is infinite, a finite approximation still yields a fixpoint in finite time, at a precision cost. | proved |
| Limit | none found | No source proves termination when working an item can add items without bound: the classic results assume a fixed equation set over a finite-height structure. The closest is Stiévenart et al. 2021, whose dependencies are discovered during the analysis itself — but over a fixed set of components. | not found |
| Most adopted | Stiévenart et al. 2021 | Worklist iteration is the standard engine of static analysis, and the exploration order is a real implementation concern: heuristics reach 20x over random, and the worklist parallelizes while converging. | survey |

## Q2 How does work trace back to a request, and how does done work close its source?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Gotel & Finkelstein 1994 | From studies of over 100 practitioners, the majority of traceability problems are pre-RS: the origins and contributors behind a requirement are not captured when they happen, and are poorly recovered afterwards. | measured |
| Upper bound | Ramesh & Jarke 2001 | Reference models synthesized from 26 organizations: the objects and link types to keep, from the low-end minimal set to the high-end design-intent set, embedded in commercial tools. | measured |
| Limit | Gotel & Finkelstein 1994 | Pre-RS links must be captured as the contributions happen; retroactive recovery is poor, so a queue rebuilt later from a conversation's residue inherits the gap by construction. | measured |
| Most adopted | GitHub Docs 2026 | The closing keyword: "Closes #10" in a pull request merged to the default branch closes the issue automatically — the post-RS half of the chain closed by a program, used across the platform. | convention |

## Q3 How is coverage of a backlog measured, including items created while working it?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Zhu, Hall & May 1997 | An adequacy criterion is both a predicate on a test set and a computable stopping rule, and coverage is the ratio of required elements exercised — the exact form the brief's measure takes. | survey |
| Upper bound | Jimenez et al. 2024 | The resolved rate: 2,294 real issues, the repository's own tests as the oracle for done, the best model of the first round at 1.96% — the strongest measured form of "done" on real work items. | measured |
| Limit | Mountain Goat 2026 | The worked set is not fixed: unknown work is discovered only during development, which is why velocity is a range and forecasts are updated as the team learns. No source in the pool measures coverage over a set that grows while it is worked. | convention |
| Most adopted | Mountain Goat 2026 | Velocity, the team's rate of closing backlog items, forecast as a range over known plus unknown work — practice's measure for exactly this question, on a list fixed at plan time. | convention |

## Q4 How do long-running agent loops decide they are done?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Cognition 2025 | The reliable long-run shape is the single-threaded linear agent: one shared context, full traces passed along, a compression model for long histories; dispersing decisions across subagents compounds errors. | convention |
| Upper bound | Yang et al. 2024 | The agent-computer interface sets the ceiling: a tailored interface reached 12.5% pass@1 on SWE-bench, far above the previous state of the art for non-interactive models — with completion still decided inside the loop. | measured |
| Limit | BabyAGI 2023 | The archetypal task-queue agent has no stop condition at all: pull the first task, execute, store, create new tasks, reprioritize, repeat — by design it runs until the operator stops paying. | convention |
| Most adopted | Manus 2025 | The production loop is action, observation, next iteration, "until the task is complete", the completion decision taken by the model inside the loop; orchestrators wrap it with iteration caps. | convention |

## Q5 How is an item too big for one job decomposed, and when?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Nau et al. 2003 | SHOP2 decomposes in execution order, generating each plan step as it will be run, so decomposition happens with the current state known — decomposition as needed, literally; awarded for distinguished performance in the 2002 planning competition. | measured |
| Upper bound | Georgievski & Aiello 2015 | Two formal models covering most HTN planners in four decades, with a five-segment comparison — domain authoring, expressiveness, competence, performance, applicability — the field's map of what decomposition can express. | survey |
| Limit | Erol, Hendler & Nau 1994 | Plan existence is undecidable in general — even propositional, two tasks per network, totally ordered; termination of decomposition is restored only by restriction, an acyclic k-level-mapping or a total order on subtasks. | proved |
| Most adopted | Khot et al. 2023 | Decomposed prompting: an LLM decomposes a complex task into simpler sub-tasks delegated to dedicated handlers, recursively decomposable when a sub-task is still hard, replaceable by symbolic functions; with Zhou et al. 2023's least-to-most as the sequential form. | measured |

Across the strands the same gap returns: the field's convergence results assume a fixed equation set (Q1), the traceability gap sits before anything is written down (Q2), the measures assume a set fixed in advance (Q3), the grey loops stop by the model's say-so or an operator's cap rather than by a rebuild (Q4), and decomposition terminates only under restriction (Q5). The hypothesis of agentic-setup#1 — a queue built by a program, worked until a rebuild adds nothing — would inherit every one of these, which is what the [baseline](baseline.md) has to beat.
