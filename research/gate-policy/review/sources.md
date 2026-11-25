# Sources

Step 2 of the review: every source fetched, with its URL, its strand, its framework and one line on what it says. The frameworks are the four of the brief: policy languages with analyzers, SMT, Datalog, model checking.

**Shape:** [sources](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/sources.md)

## Flow

| Count | |
|---|---|
| Strings run | 9 (six web, two scholar, one arXiv API; the API call returned a mismatched record and was dropped) |
| Screened by title | over 50 search results, of which 6 named leads from the brief (Cedar, OPA and Rego, Margrave, Zelkova, Soufflé, TLA+) |
| Included, formal | 9 |
| Included, grey | 8 |
| Read in the text | 16 |
| Read from the abstract (secondary) | 1 (de Moura and Bjørner 2008, read from the publisher's page) |
| Located only, left unread | 0 |

Every row below was fetched and read on 2026-11-25. No source was accepted on a search snippet alone.

## Formal

| Key | Kind | URL | Strand | Framework | What it says |
|---|---|---|---|---|---|
| Cutler et al. 2024 | method paper, OOPSLA 2024 (extended version, arXiv) | https://arxiv.org/abs/2403.04651 | 1 | policy languages with analyzers | Cedar, a policy language whose design admits a "sound and complete logical encoding, which enables precise policy analysis"; validation by schema and type; the design modeled in Lean; reads as well as and "performs far better" than OpenFGA and Rego. |
| Fisler et al. 2005 | tool paper, ICSE 2005 | https://cs.brown.edu/people/sk/Publications/Papers/Published/fkmt-verif-change-impact-xacml/paper.pdf | 1 | policy languages with analyzers | Margrave compiles XACML role policies to decision diagrams, answers queries (which roles can write a file) and change-impact between versions, with counterexamples; building the diagram took 355 ms cold, near 70 ms warm, and no property took longer than 10 ms — feasible "in an iterative refinement scenario for policy design". |
| Backes et al. 2018 | tool paper, FMCAD 2018 | https://discovery.ucl.ac.uk/id/eprint/10081411/1/Semantic-based%20Automated%20Reasoning%20for%20AWS%20Access%20Policies%20using%20SMT.pdf | 2, 5 | SMT | Zelkova translates access policies and properties into SMT and answers them soundly, e.g. "Can an arbitrary user write to this resource?"; the problem is PSPACE-complete, 99% of policy questions answer in under 160 milliseconds, and it is invoked millions of times a day at AWS. |
| Rungta 2022 | invited paper, CAV 2022 | https://link.springer.com/content/pdf/10.1007/978-3-031-13185-1_1.pdf | 2, 5 | SMT | Policy verification "is not compositional": statements each locally correct can still grant unintended access, so a global mechanism must consider all statements and their interactions; AWS runs a billion SMT queries a day; queries take "a couple hundred milliseconds to tens of seconds", so timeouts fail sound by marking the resource public. |
| de Moura and Bjørner 2008 | tool paper, TACAS 2008 | https://www.microsoft.com/en-us/research/publication/z3-an-efficient-smt-solver/ | 2 | SMT | Z3, an efficient SMT solver freely available from Microsoft Research, "used in various software verification and analysis applications" (read from the abstract: secondary). |
| Pang et al. 2019 | system paper, USENIX ATC 2019 | https://www.usenix.org/system/files/atc19-pang.pdf | 3 | Datalog (a relation-based policy store) | Google Zanzibar evaluates ACL relations with external consistency: checks use "ACL data no older than a client-specified change", so "a client can remove a user from a group and be assured that subsequent membership checks reflect that removal"; 95th-percentile latency under 10 ms over three years of production use. |
| Lamport 1994 | article, TOPLAS 16(3) | https://lamport.azurewebsites.net/pubs/lamport-actions.pdf | 4 | model checking | The temporal logic of actions: systems and their properties in one logic, so one system implementing another is logical implication; liveness and safety both expressible; rigorous reasoning is the only way to avoid subtle errors in concurrent algorithms. |
| Newcombe et al. 2015 | practice report, CACM 58(4):66-73 | https://lamport.azurewebsites.net/tla/amazon-excerpt.html (abridged; every quoted word is from the paper) | 4, 5 | model checking | TLA+ at AWS: exhaustive model checking found a DynamoDB bug whose shortest error trace had 35 steps, which design review, code review and testing had all missed; "testing the code is inadequate", the reachable states of the code are "astronomical" in number; engineers learn TLA+ in two to three weeks; whether the code implements the verified design, "we do not know". |
| Bögli et al. 2024 | systematic review, IFM 2024 (arXiv) | https://arxiv.org/abs/2411.13722 | 4 | model checking | A decade of industrial TLA+ studies: used mostly in early system design (81%); the bugs found include race conditions and deadlocks; the challenges are the steep learning curve, choosing the level of abstraction, state-space explosion, and keeping model and implementation in sync, which is "only marginally addressed". |

## Grey

Scores out of 20: authority to 4, methodology to 6, objectivity to 4, date to 1, position to 1, novelty to 2, impact to 1, outlet to 1, in that order, in steps of 0.5. A grey source under 10 is an example of practice only, not evidence.

| Key | Kind and tier | Score | Groups | URL | Strand | Framework | What it says |
|---|---|---|---|---|---|---|---|
| Cedar docs 2026 | language documentation, tier 1 | 13 | 3.5, 2.5, 3, 1, 0.5, 1, 1, 0.5 | https://docs.cedarpolicy.com/ | 1 | policy languages with analyzers | Cedar separates policy from code; the schema validates policies when they are written, not when they are evaluated; evaluation is "fast, scalable, real-time" with bounded latency; the default is deny. |
| OPA docs 2026 | product documentation, tier 1 | 13 | 3.5, 2.5, 3, 1, 0.5, 1, 1, 0.5 | https://www.openpolicyagent.org/docs/latest/ | 1 | policy languages with analyzers | OPA, a general-purpose policy engine (Rego) that decouples the decision from the enforcement point and answers queries with structured results; a CNCF graduated project. |
| OPA testing 2026 | product documentation, tier 1 | 13 | 3.5, 2.5, 3, 1, 0.5, 1, 1, 0.5 | https://www.openpolicyagent.org/docs/latest/policy-testing/ | 1 | policy languages with analyzers | `opa test` runs rules named `test_` as unit tests with mocked data and functions (`with`) and reports coverage of the lines evaluated; "use `--fail-on-empty`" so a run with no test executed fails instead of succeeding, "also useful in CI/CD pipelines". |
| OPA performance 2026 | product documentation, tier 1 | 12.5 | 3.5, 2, 3, 1, 0.5, 1, 1, 0.5 | https://www.openpolicyagent.org/docs/latest/policy-performance/ | 5 | policy languages with analyzers | "a microservice API authorization decision might have a budget in the order of 1 millisecond"; a linear fragment of Rego evaluates in near constant time, and rule indexing skips rules that cannot match. |
| Soufflé 2026 | tool site, tier 1 | 13 | 3.5, 2.5, 3, 1, 0.5, 1, 1, 0.5 | https://souffle-lang.github.io/ | 3 | Datalog | Soufflé, Datalog for large-scale static analysis, synthesized to parallel C++ by staged compilation, with provenance for explaining results. |
| learntla 2026 | tutorial site, tier 2 | 11.5 | 3, 2, 2.5, 1, 0.5, 1, 1, 0.5 | https://learntla.com/ | 4 | model checking | A free guide to TLA+: designs have flaws that reviews miss because we are only taught to "think about it really hard"; TLA+ lets you test designs directly; endorsed by AWS, Microsoft and CrowdStrike. |
| hooks 2026 | product documentation, tier 1 | 13 | 3.5, 2.5, 3, 1, 0.5, 1, 1, 0.5 | https://code.claude.com/docs/en/hooks | 4, 5 | model checking (the processes to be modeled) | Hooks run on the model's turns and block the action until they complete: PreToolUse allows or denies each tool call; a Stop hook that blocks does not end the turn — its reason comes back as the model's next instruction and the turn continues, which is the two-hook deadlock mechanism; a hook's decision time is on the per-call path. |
| cMCP 2026 | technical report, tier 3 | 12 | 3, 2, 2.5, 1, 0.5, 2, 0.5, 0.5 | https://agentrust-io.com/research/cmcp/v2/paper.pdf | 1, 5 | policy languages with analyzers | A gateway evaluating Cedar policies at the MCP tool-call boundary — principal the agent's identity, action the tool name, resource the server URL — with signed audit records and measured per-call policy evaluation; an author-prepared report, not peer reviewed, and its own limits say it does not establish complete information-flow tracking or show that every tool invocation was captured. |

## Left out, with the reason

- The ACM DL page for the Cedar OOPSLA paper (https://dl.acm.org/doi/10.1145/3649835): 403, a bot check. The CC-BY extended version on arXiv was read instead.
- CACM's own page for Newcombe et al. 2015 (https://cacm.acm.org/research/practice/how-amazon-web-services-uses-formal-methods/): 403, a bot check. Lamport's abridged excerpt of the paper, in which every quoted word is a direct quote, was read instead.
- A university mirror of the Newcombe PDF: served a file that is not a PDF; not used.
- amazon.science's page for the paper: served job listings, not the article; not used.
- Adjacent titles screened out by title in the searches (one-click formal methods, stratified abstraction, multi-step IAM attack detection, privilege reduction): later work on the same engines, but each strand's production anchor was already read, and none of the five questions needs a second one.
