# Baseline: the comparator, named

B1 is the router the lab already measures against, and with it this review is finished.

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)

## B1: Ong 2024, a router on preference data

1. A router chooses per query between one strong and one weak model, trained on human preference data with augmentation (Ong 2024, abstract).
2. It cut cost by more than 2 times in certain cases at unchanged quality, and kept its performance when the pair of models was swapped (secondary).
3. It is the baseline of the lab's specialisation review, so the two reviews share one comparator (Tewf-lab 2026 specialisation, unverifiable).

## Compared with what the review found

| Item | In B1 | The hub's flow |
|---|---|---|
| decision | one query, one pair of models | many tasks of a DAG, all agents, over rounds |
| inputs | preference data, augmented | pass rates per class, estimated from the ledger |
| method | a learned classifier over two options | a min-cost flow solved exactly |
| guarantee | none measured | proven approximation theorems for the assignment |
| measured on | benchmarks built for routing | the hub's own job ledger, at equal budget |

## What B1 lacks

- Precedence: it routes single calls, not tasks whose successors wait on them ([frame](frame.md), the problem).
- More than two agents, and a budget held across rounds rather than per call.
- A guarantee for the case where its advice is wrong, which Strand 2 of [review](review.md) found elsewhere.
- Any account of retries, measured elsewhere at up to 4.25 times the apparent cost (Fu 2026, abstract; secondary).

## How it is measured

- Both run over the same ledger of jobs, at the same dollar budget.
- The measure is cost per correct job, the metric the hub's program already computes (maestro/delegator.py, cost_per_correct).
- A call above a class ceiling counts as a violation, not as a trade, as the program's own rule says.
- Ten jobs per class, or as many as the ledger holds; the winner is the cheaper per passed job, ties broken by jobs passed.

## The review is finished

- B1 is named: Ong 2024, measured against the hub's min-cost flow on the same ledger and at the same budget.
