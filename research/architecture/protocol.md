# Protocol: how the pool was built

Twelve strings ran on six engines, five grey pages were read, and the effort bound ended the search.

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/protocol.md)

## 1. Why grey literature

- Three of the four questions ask what builders do today: patterns, guardrails, isolation, budgets.
- The pages that document a deployed agent architecture sit in no journal, and framework documentation is often the only full description of a tool.
- The object under review is grey itself: a private repository whose gate and delegator are the thing studied.
- The field's own classics of Q1 are reports and proceedings papers, so even the formal side begins in grey text.

## 2. Questions

- Q1, security and control: reference monitors, complete mediation, least privilege, guardrails, and a prose rule against an enforced hook.
- Q2, orchestration: orchestrator-worker patterns, LLM-Modulo frameworks, and tests as the oracle of generated code.
- Q3, cost: cascades and routing of model calls, and budgets held per job.
- Q4, practice: the engineering guidance of agent framework makers and laboratories on building, sandboxing and evaluating.

## 3. Existing reviews

- Not found, in these searches: a review of controlled agent architectures as a whole; the engines returned pieces, never surveys of the bundle.
- Closest kept: an industry risk list that names the failure modes without reviewing the defences (OWASP 2025).
- The sibling review of scheduling and routing holds its own pool, and is linked rather than redone ([its protocol](../dag-scheduling/protocol.md)).

## 4. Formal search

| Id | String as run | Count | New concept |
|---|---|---|---|
| F1 | crossref, 24 Nov. 2026: Saltzer Schroeder protection of information in computer systems | 10370618 | y |
| F2 | arxiv, 24 Nov. 2026: guardrails for LLM agents | 157367 | nnn |
| F3 | arxiv, 24 Nov. 2026: GuardAgent protect LLM agents meta guard tool calls | 485996 | yyn |
| F4 | arxiv, 24 Nov. 2026: LLM-Modulo Kambhampati LLMs cannot plan but can help planning sound verifiers | 1326136 | yyy |
| F5 | arxiv, 24 Nov. 2026: AutoGen enabling next-gen LLM applications via multi-agent conversation | 957231 | ynnn |
| F6 | arxiv, 24 Nov. 2026: execution-guided neural code generation tests as oracle | 1354736 | nyn |
| F7 | arxiv, 24 Nov. 2026: SWE-bench can language models resolve real-world GitHub issues | 1992926 | ynn |
| F8 | arxiv, 24 Nov. 2026: FrugalGPT | 7 | yyyy |
| F9 | openalex, 24 Nov. 2026: reference monitor computer security Anderson | 79683 | y |
| F10 | semantic-scholar, 24 Nov. 2026: prompt injection defense LLM agents | rate limited | not run |
| F11 | openaire, 24 Nov. 2026: large language model agent orchestration sandbox evaluation | timed out | not run |
| F12 | serper-scholar, 24 Nov. 2026: instruction hierarchy large language models privileged instructions safety | 10 | ynynnnnnnn |

## 5. Grey search

| Id | Producer or engine | String or what was read | Result | New concept |
|---|---|---|---|---|
| G1 | Anthropic, page read through the gateway | the building effective agents post | workflows against agents, the orchestrator-workers and evaluator patterns named | y |
| G2 | OpenAI, page read through the gateway | the practical guide to building agents, a PDF | layered guardrails, tool risk ratings, intervention on failure thresholds | y |
| G3 | LangChain, page read through the gateway | the LangGraph overview | stateful graphs mixing deterministic and model-driven steps, no prescribed architecture | y |
| G4 | OWASP, page read through the gateway | the top 10 for LLM applications, 2025 | excessive agency and unbounded consumption as named risks | y |
| G5 | the organisation's hub | the gate, the delegator and its policy table, read in the repository | ceilings, never-lists, a share cap, a path guard, a ledger; private, so unverifiable | y |

## 6. Stopping rule

- Set before the search: effort bounded at 12 strings, or saturation after 2 strings in a row that add no concept.
- The bound was reached, so the search stopped there.
- Saturation never happened: only F2 added nothing, and each of its neighbours did.
- The two failed rows count as effort, and are recorded as failures, not as zero.

## 7. Selection

- Include: works that mediate, orchestrate, verify or price the actions of model agents, with a measurement, a mechanism or a named risk.
- Exclude: recommendation agents, failure attribution and database testing, unless they measure control itself.

## 8. Quality of grey sources

- Each grey source carries a score out of 20 in eight groups, in [sources](sources.md); under 10 it counts as an example of practice only.
- The hub cannot be read without an account, so it is marked unverifiable and scored on what its own files state.

## 9. Extraction and synthesis

- One row per source in [sources](sources.md); findings by strand in [review](review.md), each figure with its key and its place.
- Abstracts and summary pages supplied most figures of the formal works, and each of those figures is marked secondary.
- Every identifier was checked before writing: each came back from an engine or was read on its own page.

## 10. Not searched, and limits

- Not searched: forward citations, snowballing, patents, works not in English, the grey engines HAL and theses.fr, and any source that needs an identity.
- Limits: F10 and F11 failed, so Semantic Scholar and OpenAIRE contributed nothing to this pool.
- Also limits: the arXiv engine parsed multi-word strings as OR, so its counts are full-text totals, and F3 refines what F2 aimed at.
- Not recorded: how many titles the giant counts would yield under phrase matching; the first page of results was screened instead.
