# Frame: what the field calls checking a gate's policy for consistency

Step 1 of the review: the question, the terms, the strands and the five properties, before any source is weighed. Evidence is in [sources](sources.md).

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md)

## The problem in one sentence

The gate, the cap and the stop check of the agentic setup are rules written as Python, each tested alone, and on the night of 25 Nov. 2026 two of them held each other: the gate closed every read at the cap while the stop check demanded a read before hand-over. The question: what does the field call a method that checks such a policy — the rules as one composed whole, including the order the hooks run in — for consistency, before a session loads it?

## The terms, defined once

- **policy as code**: access rules held in a language of their own, separated from the program's code, so they can be shared, audited and analyzed (Cutler et al. 2024; OPA docs 2026).
- **policy analyzer**: a tool that answers questions about the policy set itself — who can do what, is this version equivalent to that one — rather than about one request (Cutler et al. 2024; Fisler et al. 2005).
- **reachability query**: a question of the form "is there any request that would be allowed and reach X", answered over the policy as a whole (Backes et al. 2018).
- **change-impact analysis**: a semantic diff between two versions of a policy: which decisions changed, and why (Fisler et al. 2005).
- **model checking**: exploring every reachable state of a machine, looking for the state where a stated property breaks (Newcombe et al. 2015).
- **safety and liveness**: a safety property says a bad state is never reached; a liveness property says a good state is eventually reached. Deadlock is a liveness failure (Lamport 1994).
- **external consistency**: a change made by one process is seen, in order, by the checks another process makes (Pang et al. 2019).
- **finding**: a policy answer computed as a set — who does have access — instead of a yes/no the author had to guess first (Rungta 2022).

## What the field calls it

| The task | The field's name | Anchor |
|---|---|---|
| checking the rules as one whole | policy verification, which "is not compositional" and so needs a global mechanism over all statements and their interactions | Rungta 2022 |
| a question over all decisions at once | reachability analysis, translated to SMT | Backes et al. 2018 |
| whether two policy versions decide the same | change-impact analysis | Fisler et al. 2005 |
| the order and timing of the processes around the policy | model checking, in TLA+ | Newcombe et al. 2015 |
| one hook's write visible to another hook's read | external consistency | Pang et al. 2019 |
| deciding one request, now, before the call runs | policy evaluation in a policy engine | OPA docs 2026; Cedar docs 2026 |

## What practice calls it

- The setup's own words are gate, cap, stop check: hooks on the model's turns, each returning allow or deny for one event (hooks 2026). A Stop hook that blocks does not end the turn — its reason comes back to the model as the next instruction and the turn continues (hooks 2026). That continuation is how two hooks that are each right can hold each other: the stop check asks again, the gate denies again.
- The field's practice at the same boundary: policies evaluated at an agent's tool-call boundary — the principal is the agent, the action is the tool name, the resource is the server (cMCP 2026) — and IAM Access Analyzer's findings, "who has access", computed over whole policies in production (Rungta 2022).

## Does the repository's name match?

The repository names the pieces — gate, cap, stop check, the R-rules — and tests each alone: maestro/test_policy_gate.py for the gate, checks/test_family_gate_stop.py for the stop check. It has no name for what is missing. The field's name for it is analysis of the composed policy (Cutler et al. 2024; Rungta 2022); the issue's word, "a checker", matches the field's "analyzer".

## The strands, as sub-questions

1. What can a policy language with an analyzer prove about a whole policy set, and what does it leave to the processes around the policy? (Cedar, OPA and Rego, Margrave)
2. What can SMT decide about access policies in production, and at what cost? (Zelkova at AWS)
3. What do Datalog engines compute for policy consistency, and where does ordering come from? (Soufflé; Zanzibar's relations)
4. How does model checking catch the fault that two per-rule tests miss — a cap written by one hook, read by another — and what does it cost to learn and run? (TLA+)
5. What can run in milliseconds before every tool call, and what must move to CI? (cost)

## The five properties, and which strand can decide each

| Property | The kind of question it is | Decided by | Anchor |
|---|---|---|---|
| P1 no deadlock between hooks | liveness: at every state, if the stop check demands a call, the gate allows one | a model checker over both hooks' rules — the composition is a state machine, not a set of statements | Newcombe et al. 2015; Rungta 2022 |
| P2 at the cap, only a plan page may be written | safety invariant: no request outside the plan set is allowed while the cap holds | a policy language's analyzer (a sound, complete encoding), or SMT reachability | Cutler et al. 2024; Backes et al. 2018 |
| P3 no allowed call reaches the enforcement files | reachability over every command form the gate itself parses | SMT or Datalog evaluation over those parsed forms | Backes et al. 2018; Fisler et al. 2005 |
| P4 a new cap reaches the gate before the next call | timing between processes: one hook writes, another reads, in order | a model checker (TLA+), with external consistency as the practice's meaning of "reaches" | Newcombe et al. 2015; Pang et al. 2019 |
| P5 every way the seat can write is counted | the effects of arbitrary programs | not decidable in general: bounded by an explicit write-verb model plus the sandbox, the way the gate already enumerates write tools | Newcombe et al. 2015 |

P1 and P4 are the two faults of 25 Nov.: P1 is the deadlock itself, P4 is the second fault — the budget kept the old cap for up to ten minutes after a new cap was recorded (pilot/state-night-2026-11-25.md). Strands 1 to 3 decide what the rules permit; strand 4 decides what the processes do in time; strand 5 decides where each answer may run: per call in the hook (milliseconds), or in CI before a session loads the policy.

## Held elsewhere

- The issue: tewf-lab/agentic-setup#2, its hypothesis table of property and candidate.
- The object: .claude/policy_gate.py, checks/family_gate.py, .claude/steering_cap.py, maestro/meter_estimate.py, and pilot/state-night-2026-11-25.md, the night's record.
- The baselines: maestro/test_policy_gate.py and checks/test_family_gate_stop.py, in [baseline](baseline.md).
