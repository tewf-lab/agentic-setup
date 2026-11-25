# Review: findings by strand

It answers Q1 to Q4 of [frame](frame.md) with the 19 kept sources, in five strands, existing reviews first.

**Shape:** [review](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/review.md)

- Each key is in [references](references.md).
- A figure read in an abstract or on a summary page is marked (secondary).

## Strand 0: existing reviews

- No survey of the bundle turned up: the engines returned pieces of an architecture, never a review of the whole.
- The nearest kept work is an industry risk list, which names failure modes without reviewing defences (OWASP 2025, LLM06 and LLM10).

## Strand 1: security and control (Q1)

- Complete mediation, least privilege and fail-safe defaults were named as protection principles half a century ago (Saltzer 1975, secondary).
- A report of the same line taxonomised operating-system security flaws and treated monitor-based enforcement, in its chapters 1 and 3 (Abbott 1976, the contents page).
- Untrained models treat operator text and outside text as one priority; training a hierarchy raised robustness with little loss of capability (Wallace 2024, abstract; secondary).
- Harness context assembly can lift low-level text to instruction level: 13 attack objectives all succeeded on 6 coding harnesses, and on all 3 offering automatic permission review (He 2026, abstract; secondary).
- One guardrail agent checks a target agent's actions against written requests, and reached 98 and 83 percent accuracy on its two benchmarks (Xiang 2024, abstract; secondary).
- Guards themselves wobble: specialised tool-call guards saw false positives rise 21 to 47 points when actions arrived as shell commands (Demirkiran 2026, abstract; secondary).
- Vendors pair guardrails with authentication, authorization and strict access controls, and rate each tool by write access and reversibility (OpenAI 2025, pages 24 and 26).
- The hub's answer is the older one: a hook runs before every tool call, denies by default, and lists its allowances in code (Tewf 2026 hub, its gate file; unverifiable).
- Not found, in these searches: a measurement of a prose rule against an enforced monitor on the same agents.

## Strand 2: orchestration (Q2)

- Autoregressive models cannot plan or self-verify, so sound external verifiers must check what they propose (Kambhampati 2024, abstract; secondary).
- With a complete verifier set and re-prompting on failure, outputs stay inside what verifiers accept, with gains in four scheduling domains (Gundawar 2024, abstract; secondary).
- One framework makes agents conversable and programmable, mixing models, human input and tools (Wu 2023, abstract; secondary).
- Real repository issues judge patches by their own tests: of 2294 problems over 12 repositories, the best model resolved 1.96 percent (Jimenez 2024, abstract; secondary).
- Security can enter the loop as tests: paired insecure and secure implementations with executable checks raised Pass@1 across backbones (Wang 2024, abstract; secondary).
- One laboratory names the orchestrator-workers and evaluator-optimizer patterns and advises the simplest design that works (Anthropic 2024, the patterns section).
- Another guide sets a manager agent over specialised agents and advises exhausting a single agent first (OpenAI 2025, the orchestration chapter, page 17).
- One runtime offers graphs of shared state mixing deterministic and model-driven steps, and prescribes no agent architecture (LangChain 2026, overview).
- The hub runs the same loop with different critics: a worker proposes edits, the tests and a path guard verify, the seat judges ([frame](frame.md), the problem).

## Strand 3: cost (Q3)

- Model fees differ by two orders of magnitude, and a learned cascade matched the best single model with up to 98 percent less cost (Chen 2023, abstract; secondary).
- Retries make true cost diverge from per-call price, by up to 4.25 times on hard tasks, and forwarded failure chains lose up to 34.8 points (Fu 2026, abstract; secondary).
- Routing each trajectory step cut cost 72 percent at 97.3 percent of frontier quality, where per-step reuse of two known routers saved 31 and 44 (Paul 2026, abstract; secondary).
- Unbounded consumption is a named risk, with rate limits and budgets as the listed answer (OWASP 2025, LLM10).
- The hub prices before it runs: per-class ceilings, never-lists, a 0.20 share cap for the top model, and a dollar cap per job (Tewf 2026 hub, the policy table; unverifiable).

## Strand 4: practice, as grey literature (Q4)

- The simplest solution first, and frameworks only with understanding, since abstraction hides prompts and hides bugs (Anthropic 2024, when and how to use frameworks).
- Guardrails in layers, none sufficient alone, with human intervention set on failure thresholds and high-risk actions (OpenAI 2025, pages 25 and 31).
- The two guides agree on direct calls before frameworks and on splitting agents only when instructions stop being followed (Anthropic 2024, the whole post; OpenAI 2025, pages 8 and 16).
- Isolation appears as advice about environments, not as measurement; neither guide numbers what a sandbox is worth (Anthropic 2024, the whole post; OpenAI 2025, the whole guide).
- Not found, in these searches: measured guidance on isolated worktrees for coding agents; the studied object is the only instance kept.
