# Review: findings by strand

It groups the 22 kept sources into five strands and answers Q1 to Q4 of [frame](frame.md), with the existing reviews first.

**Shape:** [review](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/review.md)

- Each key is in [references](references.md).
- Grades are the standard's four.
- A figure read in an abstract is marked (secondary).

## Strand 0: existing reviews

- Routing and cascading across a pool of models is surveyed systematically, with a framework of when the decision is made, what feeds it and how it is computed (Moslem 2026, abstract; secondary).
- Deep reinforcement learning as a job-shop solver was already reviewed in 2018 (Cunha 2018, title; secondary).
- Scheduling under interval or bounded times is surveyed by shop environment and by measure (Allahverdi 2022, abstract).
- Not found, in these searches: a review that compares an exact assignment with a learned one on the same ledger.

## Strand 1: exact assignment under uncertainty (Q1)

- Assigning jobs to unrelated machines has a 2-approximation by rounding a linear relaxation, and no ratio under 3/2 unless P equals NP (Lenstra 1990, theorems; secondary).
- The generalized assignment problem rounds the same way into an assignment of bounded cost and bounded load violation (Shmoys 1993, abstract; secondary).
- The exact toolbox in practice answers with a status: OPTIMAL, FEASIBLE, or UNKNOWN when a limit stops it (Google 2026, the CP-SAT page).
- When job sizes are unknown, an optimal multiserver policy still exists in heavy traffic (Scully 2021, title; secondary).
- Uncertain durations are usually modelled as intervals or as distributions, and reviewed as such (Allahverdi 2022, abstract).
- Not found, in these searches: a flow model whose arc costs are estimated pass rates; the hub's combination looks unrecorded.

## Strand 2: learned schedulers against exact ones (Q2)

- Advice without a distribution is a paradigm with names for its guarantees: consistency when the advice is right, robustness when it is wrong (Mitzenmacher 2022, abstract; secondary).
- A policy trained on a constraint encoding found better solutions than static dispatching rules and than the constraint solver itself, within the same time limit, on very large instances (Tassel 2023, abstract; secondary).
- A graph-network policy was measured against the same toolbox held to 1800 seconds (Song 2022, comparison section; secondary).
- The learned policy pays in data: training needed only a generic encoding and small instances, not a simulator per problem (Tassel 2023, abstract; secondary).
- Not found, in these searches: a learned scheduler with a guarantee, measured on the same jobs as the exact one.

## Strand 3: routing, cascades and orchestration in practice (Q3)

- A cascade learned over commercial models matched the best single model with up to 98 percent less cost, or gained 4 percent accuracy at the same cost (Chen 2023, abstract; secondary).
- A router trained on preference data cut cost by more than 2 times in certain cases, and kept its edge when the pair of models was swapped (Ong 2024, abstract; secondary).
- Calibration came first in one router: isotonic regression on an uncertainty signal cut cost 31 percent at equal F1, with calibration error down from 0.12 to 0.03 (Kotte 2026, abstract; secondary).
- Retries inflate what a model seems to cost, by up to 4.25 times on hard tasks, and forwarding a failed chain to the strong model cost up to 34.8 points (Fu 2026, abstract; secondary).
- Inside one workflow the subtasks differ in difficulty, and a router over a graph of agents cut cost by up to 72.4 percent against a strong-model baseline (Liu 2026, abstract; secondary).
- One orchestration framework describes graphs of shared state that mix deterministic and model-driven steps, and prescribes no agent architecture (LangChain 2026, overview).
- A vendor names routing as a workflow pattern and sends easy calls to the small model, hard ones a tier up (Anthropic 2024, the routing section).
- One orchestration report claims 67 percent lower cost with a learned router inside its supervisor (Saini 2026, abstract; secondary).

## Strand 4: estimating per-class success from few observations (Q4)

- Completion rates from small samples are estimated with binomial intervals, compared by simulation over real large-sample sets (Sauro 2005, abstract; secondary).
- Which interval matters: exact, likelihood and other binomial intervals disagree, most in the tails (Ross 2003, abstract; secondary).
- Calibration error shrinks at the rate of the inverse cube root of the sample for isotonic regression (Kotte 2026, abstract; secondary).
- The resting review of the lab predicts pass rates from tests, with prediction-powered inference as its baseline (Tewf-lab 2026 estimators, unverifiable).
- Not found, in these searches: a study of how many observations an agent's per-class rate needs; the string that searched for it returned methods, none about agents.
