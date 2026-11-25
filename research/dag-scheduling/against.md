# Against: the evidence that cuts the other way

What would change this review's answer, and where its own sources disagree.

**Shape:** [against](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/against.md)

## Against "the exact assignment is the right default"

- Exact encodings stop scaling: on large instances the solver needs long runs or returns poor solutions, which is why practice falls back on dispatching rules (Tassel 2023, abstract; secondary).
- Routers already beat the strongest single model at equal quality on benchmarks built to test them (Moslem 2026, abstract; secondary).
- The rates the flow consumes are themselves learned and uncertain, so its optimum inherits their error, which is the subject of Q4 in [frame](frame.md).

## Against "a learned scheduler should replace it"

- The guarantees sit on the exact side: the assignment carries a proven ratio, and no learned policy in this pool carries one (Lenstra 1990, theorems; secondary).
- The same time limit is not the same budget, because training a policy consumes data and compute that the comparison rarely prices (Tassel 2023, abstract; secondary).
- What one call costs is not what a workflow costs, and the gap reaches 4.25 times on hard tasks (Fu 2026, abstract; secondary).

## Disagreements

| Point | One side | Other side |
|---|---|---|
| What a router needs | preference data and its augmentation (Ong 2024, abstract; secondary) | a calibrated uncertainty signal and nothing else (Kotte 2026, abstract; secondary) |
| Whether to use a framework | the graph runtime carries state, persistence and control (LangChain 2026, overview) | start with direct calls, since layers hide prompts and hide bugs (Anthropic 2024, when and how to use frameworks) |

- A possible reason for the first split: each side measures a different pair of models and a different benchmark.

## Against the sources themselves

- Eleven of the formal works were read at the abstract, and every figure marked secondary in [review](review.md) could not be checked against a table.
- Four of the preprints are from 2026 and unpublished outside the preprint server.
- Both lab reviews are the organisation's own, private, and read by a single reader.
- Engine totals count full text, not titles; the caveat is kept in [the architecture review's against](../architecture/against.md).
