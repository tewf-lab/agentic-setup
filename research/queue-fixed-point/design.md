# The night queue, built by a program and worked to a fixed point

**Shape:** [algorithm specification](https://github.com/Tewf/reader-ergonomics-software-design/blob/master/shapes/algorithm-specification.md)

**Problem.** From the sources of open work (the DAG's tasks and the open issues of the registered repositories),
compute the queue a steering seat works, decide when a rebuild has reached a fixed point, and measure the night's
coverage. The concept is tewf-lab/agentic-setup#1; the review behind it is [review/](review/baseline.md) (baseline B1,
the hand-listed prompt). It moves to agentic-setup once that repository has a first commit (localAI#59).

**Interface.** In `maestro/night_queue.py`:
- `Item`: a frozen dataclass with `source: str` (a repository name, or `"dag"`), `key: str` (`"#12"` or a task id),
  `title: str`, `state: str`, one of `"open"`, `"Mohamed"`, `"Desktop"`.
- `items_from_dag(tasks: list[dict]) -> list[Item]`: the tasks of `dag.toml` as `dag_stuck.load()` returns them.
- `items_from_issues(repo: str, issues: list[dict]) -> list[Item]`: issues as `gh issue list --json
  number,title,labels` returns them (`labels` a list of `{"name": str}`).
- `build(*groups: list[Item]) -> list[Item]`: one queue.
- `new_actionable(before: list[Item], after: list[Item]) -> list[Item]`, and `fixed_point(before, after) -> bool`.
- `coverage(done: int, start: int, created: int) -> float`, in [0, 1].
- `render(items: list[Item]) -> str`: the queue as markdown table rows.

**Contract.**
- Precondition: each task has `id`, `owner` and `status`; each issue has `number` and `title`.
- `items_from_dag`: one item per task whose status is not `"done"`, keyed by its id, titled by its `title` (the id if
  absent). Its state is `"Mohamed"` when the owner is `"Mohamed"` or the status is `"waiting"`; `"Desktop"` when the
  owner is `"Desktop session"`; `"open"` otherwise.
- `items_from_issues`: one item per issue, keyed `#<number>`, with source `repo`. Its state is `"Mohamed"` when a
  label is named `waits-on-mohamed`, `"Desktop"` when a label is named `desktop`, `"open"` otherwise.
- `build`: every item of every group, once per `(source, key)` (the first group that holds it wins), in the order the
  groups were given, and within a group in the order given. The group order is the priority: localAI first, then the
  lab, then the organisations.
- `new_actionable`: the items of `after` whose state is `"open"` and whose `(source, key)` is not in `before`.
- `fixed_point`: true exactly when `new_actionable(before, after)` is empty.
- `coverage`: `done / (start + created)`; `1.0` when `start + created` is 0. Raises `ValueError` when an argument is
  negative or `done` exceeds `start + created`.
- `render`: one line per item, `| <source> | <key> <title> | <state> |`, in queue order.

**Technique.** A worklist iterated to a fixed point (Kildall 1973): the seat works the queue, its work closes items
and creates others, the program rebuilds the queue from the sources, and the loop stops when a rebuild brings nothing
new the seat can act on. Termination is not guaranteed for a set that grows (the review, strand 1); the budget cap is
the variant that bounds it.

**Examples.**
- A DAG of three tasks, `a` done, `b` todo owned by `"delegator job"`, `c` waiting owned by `"Mohamed"`: two items,
  `b` open and `c` Mohamed.
- Issues `[{number: 3, title: "x", labels: []}, {number: 4, title: "y", labels: [{name: "waits-on-mohamed"}]}]` of
  `localai`: `#3` open, `#4` Mohamed.
- `build([A, B], [B', C])` where `B'` has the key of `B`: `[A, B, C]`.
- A rebuild equal to the queue before it: a fixed point. A rebuild with one new open item: not one. A rebuild whose only
  new item waits on Mohamed: a fixed point.
- `coverage(3, 5, 1) == 0.5`; `coverage(0, 0, 0) == 1.0`; `coverage(7, 5, 1)` raises.

**Properties.** `build` is idempotent: `build(build(g1, g2)) == build(g1, g2)`. `fixed_point(q, q)` holds for any `q`.

**Plan.** The test is `maestro/test_night_queue.py`, written first by the seat. A job writes `maestro/night_queue.py`,
standard library only, with a `main()` that reads `dag.toml` and prints `render(build(items_from_dag(...)))`.

**Out of scope.** Fetching the issues (the seat passes what `gh` returned); closing an item's source; decomposing an
item too big for one job (the review, strand 5: decomposition as needed, a later issue).
