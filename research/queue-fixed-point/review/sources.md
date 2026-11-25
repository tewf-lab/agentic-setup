# Sources: the pool

**Shape:** [sources](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/sources.md)

20 sources, 14 formal and 6 grey, each one fetched and read on 2026-11-25. One line per source: its strand, how far it was read, its URL, what it says. The grey sources are not scored on the 20-point scale; this review keeps the brief's one line per source, and the strands are the frame's.

## Flow

| Stage | Count |
|---|---|
| Strings run | 8 searches, beside the strands' named works |
| Screened by title | about 40 results |
| Included, formal | 14 |
| Included, grey | 6 |
| Read from the abstract or author's summary (secondary) | 7 |
| Read in the text, at least in part | 13 |
| Fetches refused, dead or wrong | 12 (ACM, IEEE, CiteSeerX, Springer, SciSpace, Atlassian, two 404s); each replaced by an open copy or left out |
| Left out | 4 |

## Formal

| Key | Strand | Read | URL | What it says |
|---|---|---|---|---|
| Kildall 1973 | 1 | text, through §3 | https://haoxintu.github.io/files/1-A%20Unified%20Approach%20to%20Global%20Program%20Optimization.pdf | The general worklist: process a node, send its optimizing information to every successor, intersect with what is there, re-queue on change; correct, and it halts because the information only descends on a finite structure. |
| Cousot & Cousot 1977 | 1 | author's summary | https://www.di.ens.fr/~cousot/COUSOTpapers/POPL77.shtml | Program properties are extremal fixpoints of systems of order-preserving functions over a complete semilattice; computed constructively by finite Kleene sequences, and by finite approximation when the sequences are infinite: termination is always purchasable, at a precision cost. |
| Stiévenart et al. 2021 | 1 | text, abstract and introduction | https://soft.vub.ac.be/Publications/2021/vub-tr-soft-21-06.pdf | A parallel worklist for modular analyses whose dependencies are only discovered during the analysis itself; convergence holds, and the order in which the worklist is explored changes performance by an order of magnitude (heuristics 20x over random). |
| Gotel & Finkelstein 1994 | 2 | text, abstract and research method | https://discovery.ucl.ac.uk/749/1/2.2_rtprob.pdf | The requirements traceability problem, from studies of over 100 practitioners: the majority of problems attributed to poor traceability come from pre-RS traceability, the links from a requirement back to its origins and the people who contributed it. |
| Ramesh & Jarke 2001 | 2 | text, abstract and introduction | https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Ramesh99.pdf | Reference models synthesized from 26 organizations: low-end traceability (minimal, compliance) against high-end (design intent), with the object and link types each development task needs; validated in case studies and built into commercial tools. |
| Jimenez et al. 2024 | 3 | abstract | https://arxiv.org/abs/2310.06770 | SWE-bench: 2,294 problems from real GitHub issues and pull requests across 12 Python repositories; a model is given the codebase and the issue, and resolved is decided by the repository's own tests; the best model of the first round resolved 1.96%. |
| Zhu, Hall & May 1997 | 3 | text, abstract and introduction | http://www.cs.toronto.edu/~chechik/courses18/csc410/p366-zhu.pdf | The survey of test coverage and adequacy: an adequacy criterion is both a predicate on test sets and a stopping rule, and coverage is the ratio of exercised elements to required elements; no computable criterion is both reliable and valid. |
| Yang et al. 2024 | 4 | abstract | https://arxiv.org/abs/2405.15793 | SWE-agent: the agent-computer interface, not only the model, sets what an agent can do; with a tailored interface an agent creates and edits files, navigates repositories and runs tests, reaching 12.5% pass@1 on SWE-bench, far above the previous state of the art for non-interactive models. |
| Wang et al. 2024 | 4 | abstract | https://arxiv.org/abs/2407.16741 | OpenHands: an open platform for generalist developer agents that write code, use a command line and browse the web, with sandboxed execution, coordination between multiple agents and benchmarks included. |
| Erol, Hendler & Nau 1994 | 5 | full text | https://www.cs.umd.edu/~nau/papers/erol1994htn.pdf | HTN planning decomposes compound tasks by methods; plan existence is undecidable in general, even propositional with two tasks per network, but decidable under a k-level-mapping (acyclic methods) or total order: decomposition terminates only under restriction. |
| Nau et al. 2003 | 5 | text, abstract and HTN background | https://www.jair.org/index.php/jair/article/download/10362/24790/19158 | SHOP2: an HTN planner that generates plan steps in the order they will be executed, so it knows the current state at each step of decomposition — decomposition as needed, literally; awarded for distinguished performance in the 2002 planning competition. |
| Georgievski & Aiello 2015 | 5 | abstract | https://arxiv.org/abs/1403.7426 | The survey of four decades of HTN planning: two formal models covering most planners, concepts for reading their search spaces, and a comparison on domain authoring, expressiveness, competence, performance and applicability. |
| Khot et al. 2023 | 5 | abstract | https://arxiv.org/abs/2210.02406 | Decomposed prompting: decompose a complex task by prompting into simpler sub-tasks delegated to dedicated LLM handlers, recursively decomposable when a sub-task is still hard, and replaceable by symbolic functions. |
| Zhou et al. 2023 | 5 | abstract | https://arxiv.org/abs/2205.10625 | Least-to-most prompting: break a problem into a series of simpler subproblems solved in sequence, each facilitated by the answers to the previous ones; generalizes to problems harder than the exemplars (SCAN at 99%+ against 16% for chain-of-thought). |

## Grey

| Key | Strand | Read | URL | What it says |
|---|---|---|---|---|
| GitHub Docs 2026 | 2 | full text | https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue | Closing keywords: a pull request whose description says "Closes #10" (up to ten issues) closes them automatically when merged into the default branch; keywords in other branches are ignored. |
| Anthropic 2024 | 4 | text, first half | https://www.anthropic.com/engineering/building-effective-agents | Workflows orchestrate LLMs through predefined code paths, agents direct their own processes; find the simplest solution possible and add complexity only when needed, for agentic systems trade latency and cost for task performance. |
| Cognition 2025 | 4 | full text | https://cognition.ai/blog/dont-build-multi-agents | Principles of context engineering for long-running agents: share context and full traces, because actions carry implicit decisions that conflict when dispersed; the single-threaded linear agent, with a compression model for long histories, is the reliable default, and multi-agent architectures remain fragile. |
| Manus 2025 | 4 | text, first half | https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus | The production agent loop is action, observation, next iteration, "until the task is complete", decided inside the loop; the engineering is context engineering: stable prompt prefix, append-only context, masked rather than removed tools, around a roughly 100:1 input-to-output token ratio. |
| BabyAGI 2023 | 4 | full README | https://github.com/yoheinakajima/babyagi_archive | The minimal task-queue agent, 140 lines: an infinite loop that pulls the first task, executes it, stores the result, then creates new tasks and reprioritizes the list from the objective and the last result; designed to run continuously, with a warning about the API cost of doing so. |
| Mountain Goat 2026 | 3 | text, first half | https://www.mountaingoatsoftware.com/agile/agile-planning-and-forecasting | Milestone forecasting for a backlog: known work (the items already identified) plus unknown work (work discovered only during development), velocity as a range rather than an average, and a forecast updated as the team learns. |

## Left out, with the reason

- Bourdoncle 1993, "Efficient chaotic iteration strategies with widenings": the classic on iteration strategies and weak topological ordering; every copy found refused the fetch (CiteSeerX rate-limited, the Springer DOI resolved to an unrelated book). Its ground is covered by Stiévenart et al. 2021, which builds on it.
- Kam & Ullman 1976, "Global data flow analysis and iterative algorithms": paywalled at SIAM, no open copy located; Kildall 1973 and Stiévenart et al. 2021 cover the same ground for this review.
- Atlassian's velocity page: redirected to an advertising tracker instead of the article; Mountain Goat's planning and forecasting guide was read instead.
- AutoGPT: not fetched; the archived BabyAGI is the older and smaller task-queue loop and was read in its place.
