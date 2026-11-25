# Protocol: how the pool was built

Twelve strings ran across six engines and five grey pages were read, and the search stopped at its effort bound.

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/protocol.md)

## 1. Why grey literature

- Three of the four questions are about practice: what routers, cascades and orchestrators do today.
- The engineering posts that document a deployed cascade sit in no journal, and the frameworks' own documentation is the only full description of some tools.
- The object itself is grey: a private repository whose planner is what this review studies.
- The two lab reviews this one rests on are grey in the same way, and are named as sources rather than rediscovered.

## 2. Questions

- Q1, exact methods: assignment, flow, constraint solving, and approximations under uncertainty.
- Q2, learned methods: policies and advice, measured against an exact solver at equal budget.
- Q3, practice: routing, cascades and orchestration of calls to models.
- Q4, estimation: a per-class success rate from few observations.

## 3. Existing reviews

- Found, three: a systematic survey of routing and cascading across models, in TMLR 2026 (Moslem 2026).
- Found as well: a literature review of deep reinforcement learning as a job-shop solver (Cunha 2018).
- Found as well: a survey of scheduling under interval or bounded times (Allahverdi 2022).
- Not found: a review of an exact assignment against a learned one on the same ledger, nor one of pass-rate estimation per class for agents.

## 4. Formal search

| Id | String as run | Count | New concept |
|---|---|---|---|
| F1 | openalex, 24 Nov. 2026: approximation algorithms for scheduling unrelated parallel machines | 8331 | y |
| F2 | arxiv, 24 Nov. 2026: LLM cascade cost efficient inference routing | 639462 | nny |
| F3 | arxiv, 24 Nov. 2026: RouteLLM learning to route LLMs preference data | 1091397 | nnn |
| F4 | arxiv, 24 Nov. 2026: FrugalGPT | 7 | yyyy |
| F5 | arxiv, 24 Nov. 2026: RouteLLM | 8 | nny |
| F6 | crossref, 24 Nov. 2026: algorithms with predictions Mitzenmacher | 427988 | yy |
| F7 | crossref, 24 Nov. 2026: approximation algorithm generalized assignment problem Shmoys Tardos | 1803266 | ynn |
| F8 | crossref, 24 Nov. 2026: stochastic scheduling uncertain processing times survey | 2960264 | yyy |
| F9 | semantic-scholar, 24 Nov. 2026: learning-augmented algorithms scheduling predictions | rate limited | not run |
| F10 | openaire, 24 Nov. 2026: DAG scheduling heterogeneous processors list scheduling | timed out | not run |
| F11 | serper-scholar, 24 Nov. 2026: deep reinforcement learning job shop scheduling compared with exact solver | 10 | ynnynnynny |
| F12 | serper-scholar, 24 Nov. 2026: estimating pass rate of a model from few samples confidence interval | 10 | nyyynnnnnn |

## 5. Grey search

| Id | Producer or engine | String or what was read | Result | New concept |
|---|---|---|---|---|
| G1 | Google, pages read through the gateway | the CP-SAT page of the OR-Tools manual | the statuses and limits of the exact toolbox in practice | y |
| G2 | LangChain, pages read through the gateway | the LangGraph overview | graphs of state mixing deterministic and model-driven steps | y |
| G3 | Anthropic, pages read through the gateway | the building effective agents post | routing named as a workflow, capability priced against cost | y |
| G4 | the organisation's lab | the specialisation review in recursive-delegation | its baseline is a router; private, so unverifiable without an account | y |
| G5 | the organisation's lab | the estimators review in probabilistic-oracles | its baseline is a prediction-powered pass rate; unverifiable | y |

## 6. Stopping rule

- The same rule as [the architecture protocol](../architecture/protocol.md) applies here, set before the search.
- It stopped at the effort bound; only F3 added nothing, never two strings in a row.
- The two failed rows (F9 and F10) count as effort, recorded as failures, not as zero.

## 7. Selection

- Include: works that assign, schedule, route or estimate for model calls or for machines, with a cost, a rate or a guarantee.
- Exclude: privacy of routing metadata, network routing and preference learning, unless they measure delegation itself.

## 8. Quality of grey sources

- Grey sources are scored as in [the architecture protocol](../architecture/protocol.md), out of 20 over eight groups, with the scores in [sources](sources.md).
- The two lab reviews cannot be read without an account, so they are marked unverifiable and scored on what this hub states about them.

## 9. Extraction and synthesis

- One row per source in [sources](sources.md), findings by strand in [review](review.md), the same layout as [the architecture protocol](../architecture/protocol.md).
- Abstracts supplied most figures, and each of those is marked secondary.
- Identifiers were checked before writing: each came from an engine or its own page.

## 10. Not searched, and limits

- Not searched, the same ground as [the architecture protocol](../architecture/protocol.md): forward citations, snowballing, patents, non-English works, HAL and theses.fr, sources needing an identity.
- Limits: F9 and F10 failed, so learning-augmented scheduling rests on two works and OpenAIRE on none.
- Also limits: one earlier variant of F1, with 9730 works and the same first result, is not a row of its own.
- The first failed attempts of F9 and F10, which failed like their recorded rows, are not rows of their own either.
- Not recorded: the engines' totals count full text, not titles, so a count in the thousands says nothing about how many hits were on topic.
