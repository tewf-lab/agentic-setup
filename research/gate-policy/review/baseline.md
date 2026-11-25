# Baseline

Step 5 of the review: the baseline the checker is compared against, named. Evidence is in [sources](sources.md).

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)

**Baseline:** B1, the per-rule unit tests the gate has today — maestro/test_policy_gate.py for the gate alone, checks/test_family_gate_stop.py for the stop check alone, one synthetic payload per rule — and the measure to beat: the deadlock of 25 Nov. 2026, found before a session loads the policy.

## B1: the per-rule unit tests, each rule alone

1. maestro/test_policy_gate.py calls the gate's decision with synthetic tool payloads against a fixed budget file, one rule per test: a plan page is allowed, a big edit is delegated, an enforcement file is refused, chains are judged part by part, and at a red budget the small edits close too.
2. checks/test_family_gate_stop.py calls the stop check with synthetic transcripts, R4 alone: writing without reading a shape is blocked, a shape read in the session lets the turn end, a delegated worker is judged by its acceptance instead, and a second stop is let through.
3. Both suites passed on the night of 25 Nov. 2026 while the composition deadlocked: each rule is right alone, and no test feeds one rule's output to the other as input.
4. The faults were found at run time and fixed by hand — the cap hook now rewrites the budget at once, and the stop check stands down at red, both marked "found 2026-11-25" in the files (tewf-lab/agentic-setup#2) — which is what B1 cannot do: it tests the rules, not their combination.

The neighbour kept apart, the field's own version of the same baseline: **B2, `opa test`** — a policy engine's unit tests, with mocked data (`with`), coverage of evaluated lines, and "use `--fail-on-empty`" so a run with no test executed fails, "also useful in CI/CD pipelines" (OPA testing 2026). B2 has B1's shape and B1's limit: it checks the rules that are written, one at a time, and composition is out of its frame (Rungta 2022).

## Compared with what the review found

| Item | In B1 | Fit |
|---|---|---|
| each rule alone, tested | yes, one synthetic payload per test | matches (OPA testing 2026) |
| the rules as composed | no test feeds the gate's denial to the stop check's demand | lacks (Rungta 2022: not compositional, a global mechanism needed) |
| at the cap, only a plan page is written | the red-budget test asserts one denial, not the invariant over all requests | lacks (Backes et al. 2018) |
| no allowed call reaches the enforcement files | the enforcement paths are listed and tested one at a time, not over every parsed command form | in part (Backes et al. 2018; Fisler et al. 2005) |
| a new cap reaches the gate before the next call | untested: the night's stale budget held the old cap for up to ten minutes | lacks (Pang et al. 2019; Newcombe et al. 2015) |
| every way the seat can write is counted | the gate's own list of write tools, tested per tool | in part (cMCP 2026 names the same limit) |
| the cost of checking | nothing new: both suites already run in CI | matches (OPA performance 2026) |

## What B1 lacks

- Composition: no test runs the two hooks against each other, and the field is explicit that per-statement correctness does not compose (Rungta 2022).
- A reachability question: nothing asks "is there any request, in any parsed command form, that is allowed and reaches the enforcement files" (Backes et al. 2018).
- Change-impact: a policy edit — the cap hook's rewrite, the stop check's stand-down — is verified by rerunning the same per-rule tests, not by a semantic diff of what the rules now permit (Fisler et al. 2005).
- Timing: no test bounds how long one hook's write stays unread by the other; the measure the field gives this is external consistency (Pang et al. 2019).
- A regression fixture: the night's deadlock exists as prose (pilot/state-night-2026-11-25.md), not as a case a checker must catch.

## How it is measured

- The checker must find, from the policy files alone — the gate, the stop check, the cap hook, the meter — in CI, before any session loads the policy: (a) the deadlock, at a red budget the gate denying the shape read the stop check demands before hand-over; (b) the timing fault, a cap recorded by one hook unread by the gate until the meter's next tick.
- B1 demonstrably passes while both faults are present: each suite tests its own rule, and both passed that night. The checker beats B1 exactly when it fails those two cases, and passes them once the hand fixes are in — the fixed files of 25 Nov. are the negative control.
- The cost side is part of the measure: whatever does this must not sit before every tool call — the decision stays in the gate's milliseconds (OPA performance 2026; Cedar docs 2026), the analysis runs in CI, the pattern of `opa test --fail-on-empty` (OPA testing 2026) and of Rungta's queries at AWS (Rungta 2022).

## The review is finished

The baseline is named, B1 with B2 as the field's own version of it, and the measure is the deadlock of 25 Nov. 2026 found before a session loads the policy, in CI, from the policy files alone. The next work is the design of the checker in tewf-lab/agentic-setup#2.
