# Brief: review the literature for checking a gate's policy for consistency

**Shape:** [brief](https://github.com/Tewf/ai-augmented-project/blob/1a749dfcc4e182c7fe055e00aff3d937a68e5978/shapes/brief.md), pinned at the commit that added Cost, after v0.1.0.
**Kind:** review
**Repo:** localAI (the review moves to tewf-lab/agentic-setup once that repository has a first commit, localAI#59)
**Depends on:** none
**Outcome:** pending

## Task

tewf-lab/agentic-setup#2: the gate, the cap and the stop check of an agentic setup are rules written as Python, each
tested alone, and nothing checks how they combine. On the night of 25 Nov. 2026 two of them deadlocked: at the cap
the gate closed every read, and the stop check asked for a read before any hand-over. Review the grey and academic
literature on checking such a policy for consistency, before any design.

## Decided

- Proof: reference (every claim cites a source that was fetched and read).
- Frameworks: each source names its framework (policy languages with analyzers, SMT, Datalog, model checking).
- Legality: none.
- Shapes to read: [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md),
  [sources](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/sources.md),
  [state-of-the-art](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/state-of-the-art.md),
  [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)
- The strands, from the issue:
  1. policy languages with analyzers: Cedar (Cutler et al., OOPSLA 2024), OPA and Rego, Margrave (Fisler et al.,
     ICSE 2005);
  2. SMT for access policies in production: Zelkova at AWS (Backes et al., FMCAD 2018);
  3. Datalog engines (Soufflé) and their use for policy consistency;
  4. TLA+ for timing properties between processes (a cap recorded by one hook, read by another);
  5. the cost of each: the hook decides before every tool call, so a decision stays in milliseconds, with the analysis
     run in CI.
- The properties to place, from the issue: P1 no deadlock between hooks; P2 at the cap only a plan page may be written;
  P3 no allowed call reaches the enforcement files; P4 a new cap reaches the gate before the next call; P5 every way
  the seat can write is counted.
- Write only under `work/2026-11-25_gate-policy-review/review/`. Do not edit `test_review.py`.

## To find

Four files under `review/`, each opening with a `**Shape:**` line that names its review shape:

- `frame.md`: the question, the strands, the five properties and which strand can decide each;
- `sources.md`: every source fetched, one line each, with its URL, its strand and one line on what it says; at least 15;
- `state-of-the-art.md`: per strand, the best current method and its known limits;
- `baseline.md`: the named baseline (the per-rule unit tests the gate has today) and the measure a checker must beat
  (the deadlock of 25 Nov. found before a session loads the policy).

## Checks

- `python3 -m unittest discover -s work/2026-11-25_gate-policy-review -p test_*.py`: four files with Shape lines, 15 URLs, a named baseline.

## Cost

- Tokens: pending
- Dollars: pending
- Minutes: pending
- Produced: pending
