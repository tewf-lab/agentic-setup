# The organisation of an agentic setup

Who does what in a setup that holds the nine practices of the [standard](standard.toml): one person, two model sessions, the programs that enforce, and the workers.

**Shape:** [figure](https://github.com/Tewf/reader-ergonomics-presentations/blob/master/shapes/figure.md)

**The person sets goals and limits, the steering seat plans and dispatches, programs assign, check and guard, and the workers do the bulk.**

![An organisation chart: a person above two model sessions, the programs that enforce the practices, five kinds of worker, the gateway and CI.](organisation.svg)

## What the chart shows

- Person: goals, caps, approvals
- Maintainer session: changes the enforcement
- Steering seat: plans, decides, small edits
- Gate and hooks: S1 gate, S7 cap, stop checks
- Exact method: S2 assigns, S3 accepts, S4 scope, S5 ledger, S6 DAG
- Task command: S8 template and families
- Worker, flat plan: the bulk
- Worker, pay per token: when it is cheaper per answer
- Worker, data kept local: personal data
- Worker, local model: free, offline
- Worker, frontier model: escalation only
- Gateway: push, issues, paid compute
- CI on the server: S9 re-checks every push

Colours: a person in orange, a model in blue, a program in green; each box also names its kind.

An implementation fills each role with its own agents and programs.

<details><summary>Graphviz source</summary>

```dot
digraph organisation {
  rankdir=TB; nodesep=0.35; ranksep=0.5;
  node [shape=box, style="rounded,filled", fontname="Inter", fontsize=11, fontcolor="#1F2328"];
  edge [fontname="Inter", fontsize=9, color="#3D434B", fontcolor="#3D434B"];
  person [label="Person (person)\ngoals, caps, approvals", fillcolor="#FBEDE4", color="#B4541A", penwidth=2];
  maintainer [label="Maintainer session (model)\nchanges the enforcement", fillcolor="#E8EEF8", color="#2F5DA8"];
  seat [label="Steering seat (model)\nplans, decides, small edits", fillcolor="#E8EEF8", color="#2F5DA8"];
  gate [label="Gate and hooks (program)\nS1 gate, S7 cap, stop checks", fillcolor="#E6F2EA", color="#2E7D4F"];
  method [label="Exact method (program)\nS2 assigns, S3 accepts,\nS4 scope, S5 ledger, S6 DAG", fillcolor="#E6F2EA", color="#2E7D4F"];
  task [label="Task command (program)\nS8 template and families", fillcolor="#E6F2EA", color="#2E7D4F"];
  flat [label="Worker, flat plan (model)\nthe bulk", fillcolor="#E8EEF8", color="#2F5DA8"];
  paid [label="Worker, pay per token (model)\nwhen it is cheaper per answer", fillcolor="#E8EEF8", color="#2F5DA8"];
  data [label="Worker, data kept local (model)\npersonal data", fillcolor="#E8EEF8", color="#2F5DA8"];
  local [label="Worker, local model (model)\nfree, offline", fillcolor="#E8EEF8", color="#2F5DA8"];
  frontier [label="Worker, frontier model (model)\nescalation only", fillcolor="#E8EEF8", color="#2F5DA8"];
  gateway [label="Gateway (program)\npush, issues, paid compute", fillcolor="#E6F2EA", color="#2E7D4F"];
  ci [label="CI on the server (program)\nS9 re-checks every push", fillcolor="#E6F2EA", color="#2E7D4F"];
  person -> seat [label="prompt and cap"];
  person -> maintainer [label="requests"];
  maintainer -> gate [label="maintains"];
  gate -> seat [label="mediates every call"];
  seat -> task [label="starts and closes tasks"];
  seat -> method [label="dispatches"];
  method -> flat [label="assigns"];
  method -> paid [label=""];
  method -> data [label=""];
  method -> local [label=""];
  method -> frontier [label="after failures", style=dashed, color="#6A6D77"];
  method -> gateway [label="push after merge"];
  seat -> gateway [label="issues, push"];
  person -> gateway [label="approves money, public", style=dashed, color="#6A6D77"];
  gateway -> ci [label="each push"];
}
```

</details>
