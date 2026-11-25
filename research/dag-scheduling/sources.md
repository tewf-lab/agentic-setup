# Sources: the pool

Seventeen formal works and five grey ones were kept, from 42 titles screened.

**Shape:** [sources](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/sources.md)

## Flow

| Stage | Count |
|---|---|
| Strings run | 12 |
| Screened by title | 42 |
| Included, formal | 17 |
| Included, grey | 5 |
| Grey below 10 of 20, examples only | 0 |
| Read from the abstract (secondary) | 17 |
| Located only, not read | 27 |

## Formal

| Key | Kind | Found via | Grade or use | Used in |
|---|---|---|---|---|
| Lenstra 1990 | journal article | F1 | theorem, read as secondary | review, state-of-the-art |
| Shmoys 1993 | journal article | F7 | theorem, read as secondary | review |
| Scully 2021 | journal article | a crossref check beside F6 | measured, descriptive | review |
| Allahverdi 2022 | survey | F8 | map of the uncertain-time field | review, state-of-the-art |
| Mitzenmacher 2022 | survey in CACM | F6 | the paradigm of advice | review, state-of-the-art |
| Cunha 2018 | literature review | F11 | existing review | review |
| Song 2022 | journal article | F11, identifier checked | measured, at a time limit | review, state-of-the-art |
| Tassel 2023 | conference paper | F11, identifier checked | measured, at the same limit | review, state-of-the-art |
| Sauro 2005 | conference paper | F12 | measured, descriptive | review, state-of-the-art |
| Ross 2003 | journal article | F12 | method for intervals | review |
| Chen 2023 | preprint | F4 | measured cascade | review, state-of-the-art |
| Ong 2024 | preprint | its abstract page, read for B1 | measured router | baseline, review |
| Moslem 2026 | survey, TMLR | F2 | existing review | review |
| Kotte 2026 | preprint | F2 | measured, calibrated router | review, state-of-the-art |
| Fu 2026 | preprint | F4 | measured, cost of retries | review, state-of-the-art |
| Liu 2026 | preprint | F4 | measured, routing inside a graph | review |
| Saini 2026 | preprint | F5 | measured orchestration | review |

## Grey

Grey sources are scored out of 20 across the eight groups, in the order set by [the architecture review's sources](../architecture/sources.md).

| Key | Kind and tier | Score | Groups | Note |
|---|---|---|---|---|
| Google 2026 | documentation, tier 1 | 14 | 4, 2, 3, 1, 1, 1, 1, 1 | the solver's own manual, read on the page |
| LangChain 2026 | documentation, tier 1 | 13 | 3, 2, 3, 1, 1, 1, 1, 1 | vendor overview of graph orchestration, read on the page |
| Anthropic 2024 | engineering post, tier 1 | 15.5 | 4, 3, 3, 1, 1, 1.5, 1, 1 | patterns drawn from dozens of teams, routing section read |
| Tewf-lab 2026 specialisation | review, tier 2 | 14 | 3, 4, 3, 1, 1, 1, 0.5, 0.5 | the lab's own review, private, unverifiable without an account |
| Tewf-lab 2026 estimators | review, tier 2 | 14 | 3, 4, 3, 1, 1, 1, 0.5, 0.5 | same, its baseline a prediction-powered pass rate |

## Left out, with the reason

- A preprint on routing inside one trajectory, found at F4: its record was cut before the authors, so no key could be made.
- Seven titles of F11, among them a design-patterns survey and a solver benchmark: the same family as the kept works, no concept added.
- The Cambridge chapter of the same authors as the kept CACM piece, found at F6: one of the two suffices.
- Two titles of F7, a reference-work entry and a k-median paper: the query reached them by name match only.
- Two titles of F8, a French thesis and a port study: shop floors, not agents, though the thesis does price a probability of finishing.
- Eight titles of F12, among them Hanczar 2013, bootstrap guides and four pass-rate studies of other domains: methods or fields aside from this one.
- Six titles of F2, F3 and F5, on private inference, on router metadata, on network routing and on preference learning: off topic.
- Twenty-seven titles in all were located and not read; every one was screened by title at its string.
