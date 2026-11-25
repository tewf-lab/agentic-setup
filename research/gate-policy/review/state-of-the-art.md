# State of the art

Step 4 of the review: per strand, the best current method and its known limits. Holders are keyed to [sources](sources.md).

**Shape:** [state of the art](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/state-of-the-art.md)

## Q1: what a policy language's analyzer proves

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Cedar (Cutler et al. 2024) | a "sound and complete logical encoding" lets an analyzer prove things of the whole policy set — e.g. that a refactor leaves the permitted decisions unchanged — and the design itself is modeled in Lean | strongest |
| upper bound | Margrave (Fisler et al. 2005) | queries over all roles and change-impact between policy versions, with counterexamples, at interactive speed: no property over its examples took longer than 10 ms | strong, on an older language |
| limit | Cedar docs 2026; cMCP 2026 | validation checks a policy against a schema at write time; the analyzer's frame is the policy set. It says nothing about the processes around the policy — which hook runs first, what the stop check demands — and cMCP, the closest practice to the gate's boundary, states its own limit: it does not show every tool invocation was captured | the known bound |
| most adopted | OPA (OPA docs 2026) | the general-purpose engine, decoupled from the code, CNCF graduated, with `opa test` for per-rule unit tests and coverage (OPA testing 2026) | the practice |

The strand's answer: an analyzer proves the policy set correct by construction and answers whole-set questions — but the night's fault was not in the gate's rule set; it was in the composition with another hook, which this strand does not see.

## Q2: what SMT decides, and at what cost

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Zelkova (Backes et al. 2018) | policies and properties translated to SMT and answered soundly — "Can an arbitrary user write to this resource?" — at production scale, millions of invocations a day | strongest |
| upper bound | Rungta 2022 | a billion queries a day at AWS; the question changed from guessed properties to computed findings ("who has access?"); portfolio solvers, 30-second budgets, sound fallback on timeout | strong |
| limit | Rungta 2022 | queries take "a couple hundred milliseconds to tens of seconds", solver runtimes are not monotonically better across versions, and a timeout fails sound by marking the resource public — an SMT answer is a CI answer, not a per-call decision | the known bound |
| most adopted | Z3 (de Moura and Bjørner 2008) | the solver under such systems, "used in various software verification and analysis applications" | the practice |

The strand's answer: SMT decides P2 and P3 exactly — a reachability query over the policy set, in CI — and the sound-but-slow failure mode is exactly why it cannot sit before every tool call.

## Q3: what Datalog computes, and where ordering comes from

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Zanzibar (Pang et al. 2019) | a relation-based policy store evaluated at global scale, with external consistency — checks respect "ACL data no older than a client-specified change" — at under 10 ms, 95th percentile, over three years | strongest |
| upper bound | Soufflé (Soufflé 2026) | Datalog synthesized to parallel C++ for large-scale static analysis, with provenance to explain results | strong on speed, no policy-consistency result in the pool |
| limit | Pang et al. 2019 | the ordering in Zanzibar comes from the storage layer — timestamps and change tokens — not from the policy language itself; no fetched source shows a Datalog engine deciding a timing property between two processes | the known bound |
| most adopted | none found | the pool holds no Datalog engine deciding a hook policy's consistency in production; the practice anchors are strand 1's engines | none found |

The strand's answer: Datalog evaluates a composed policy cheaply and explains itself (provenance), which suits P1 and P3 as a query engine — but P4, the timing fault, is decided by whatever orders the writes, and in the pool that is never the Datalog itself.

## Q4: how model checking catches what two per-rule tests miss

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Newcombe et al. 2015 | exhaustive model checking found a DynamoDB bug whose shortest error trace had 35 steps, missed by design review, code review and testing; "testing the code is inadequate" because the reachable states are "astronomical" in number | strongest |
| upper bound | Bögli et al. 2024 | a decade of industrial use: race conditions and deadlocks among the found bugs, across cloud systems, mostly at the early design stage (81%) | strong |
| limit | Bögli et al. 2024; Newcombe et al. 2015 | the steep learning curve, the choice of abstraction, state-space explosion, and model-implementation sync "only marginally addressed"; on whether the code implements the verified design, "we do not know" | the known bound |
| most adopted | TLA+ (learntla 2026) | the method AWS, Microsoft and CrowdStrike endorse; a free guide exists because the community pushes the learning curve down | the practice |

The strand's answer: the deadlock of P1 and the stale cap of P4 are exactly this kind of fault — two processes each correct, wrong together — and the field's tool for them is a model checked exhaustively against both hooks' rules, in CI, not in the hook.

## Q5: what runs in milliseconds, and what moves to CI

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | OPA performance 2026 | "a microservice API authorization decision might have a budget in the order of 1 millisecond"; a linear fragment evaluates in near constant time, and rule indexing skips what cannot match | strongest |
| upper bound | Cedar docs 2026; Backes et al. 2018 | bounded-latency evaluation as a design goal, and Zelkova's measured 99% under 160 ms — engine-class decisions reach milliseconds, solver-class answers do not | strong |
| limit | Rungta 2022; hooks 2026 | SMT queries run hundreds of milliseconds to tens of seconds with sound timeouts, and a hook blocks the action until it completes — so the analysis cannot sit on the per-call path | the known bound |
| most adopted | OPA (OPA docs 2026; OPA testing 2026) | the split itself is the practice: an engine decides per call, and the analysis — `opa test` with coverage, `--fail-on-empty` in CI — runs before deployment | the practice |

The strand's answer: the field's shape is two-tier, and the issue's design sketch matches it — a thin policy decision in the hook (milliseconds), and the consistency analysis run in CI, where seconds are free.

## The strands together

Deciding per call and analyzing in CI are different tools, and every strand puts the five properties on one side or the other: P1 and P4 to the model checker, P2 and P3 to the analyzer or the solver (Cedar's encoding, Zelkova's queries), P5 to neither — bounded by an explicit write-verb model and the sandbox, with Newcombe's honest limit, "we do not know", as the ceiling (Newcombe et al. 2015).
