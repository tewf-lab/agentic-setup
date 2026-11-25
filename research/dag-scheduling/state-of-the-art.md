# State of the art: the records per question

For each question the best evidence, kept apart from the practice most adopted.

**Shape:** [state-of-the-art](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/state-of-the-art.md)

## Q1

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Lenstra 1990 | a 2-approximation by rounding a linear relaxation, for machines that differ per job (secondary) | supported with caveat |
| Upper bound | Lenstra 1990 | no polynomial ratio under 3/2 unless P equals NP (secondary) | supported with caveat |
| Limit | Tassel 2023 | exact encodings stop scaling on large instances | supported with caveat |
| Most adopted | Google 2026 | model the problem, then let a constraint solver run to a limit | convention |

## Q2

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Tassel 2023 | a policy trained on the encoding beats the solver at the same time limit, on very large instances | measured |
| Upper bound | Mitzenmacher 2022 | advice-based algorithms admit provable consistency and robustness (secondary) | supported with caveat |
| Limit | none found | no guarantee measured for a learned scheduler on the same jobs | convention |
| Most adopted | Song 2022 | graph-network policies, benchmarked against the exact toolbox at a fixed limit | measured |

## Q3

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Chen 2023 | a learned cascade matches the best single model at up to 98 percent less cost | measured |
| Limit | Fu 2026 | per-call prices understate workflow cost by up to 4.25 times | measured |
| Most adopted | Anthropic 2024 | route the easy calls down, the hard calls up | convention |

## Q4

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Sauro 2005 | binomial intervals for a rate from small samples, compared by simulation | measured, descriptive |
| Upper bound | Kotte 2026 | isotonic calibration error falls as the inverse cube root of the sample | measured |
| Limit | none found | no study of the observations a per-class agent rate needs | convention |
| Most adopted | Tewf-lab 2026 estimators | a pass rate predicted from the tests, its baseline prediction-powered inference | convention |
