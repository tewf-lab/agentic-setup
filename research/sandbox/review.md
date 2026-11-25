# Review: a task sandbox built from the template — the data gathering of issue 9

A literature review in four steps — Frame, Literature review, State of the art, Position — on what issue 9 asks for: a task sandbox built from the template, holding a task's commands to the scope its own brief declares. Every claim cites a page fetched for this review, academic and grey; the URLs are in [Sources](#sources), read 25 Nov. 2026. The acceptance is `research/sandbox/test_review.py`.

## Frame

Step 1: the question, the terms, the strands and the properties, before any source is weighed.

### The problem in one sentence

`standard.toml` requires of practice S4 ("scope") that "a task's changes are held to the scope it declared", and sources the practice to "least privilege, Saltzer and Schroeder 1975; issue 9 for the sandbox" — yet in this family a task's scope is prose in its brief ("Edit only these paths", "Never touch", "Scratch files go only under `.scratch/`, which is never committed nor judged"), read by the delegator *after* the work is done. Nothing holds the commands *while they run*. The question: given the scope a task's brief already declares, what mechanism holds that task's commands to the declared scope as they run — and what does the holding cost per call?

The brief of the task that wrote this review carries exactly such a list, which makes the object of study and the instrument of study the same shape: an allowlist of paths to edit, a list never to touch, and a scratch exception that is writable but unjudged. A template (practice S8) produces that list; the sandbox would be the thing that consumes it.

### The terms, defined once

- **sandbox**: a mechanism that confines a program's accesses to a declared subset. The bubblewrap authors are precise about what their tool is not: "bubblewrap is not a complete, ready-made sandbox with a specific security policy", and the protection "is entirely determined by the arguments passed to bubblewrap" ([bubblewrap README](https://github.com/containers/bubblewrap)).
- **complete mediation**: "Every access to every object must be checked for authority" — "the primary underpinning of the protection system" (Saltzer and Schroeder 1975).
- **least privilege**: "Every program and every user of the system should operate using the least set of privileges necessary to complete the job" (Saltzer and Schroeder 1975).
- **fail-safe defaults**: "Base access decisions on permission rather than exclusion"; "the default situation is lack of access" (Saltzer and Schroeder 1975).
- **capability**: "an unforgeable ticket, which when presented can be taken as incontestable proof that the presenter is authorized to have access to the object named in the ticket", against an access control list, "a list of principals that are authorized to have access to some object"; "capability systems are ticket-oriented, while access control list systems are list-oriented" (Saltzer and Schroeder 1975). In Capsicum, "file descriptors into capabilities" that "must be presented to perform an action" ([capsicum(4)](https://man.freebsd.org/cgi/man.cgi?query=capsicum)).
- **ambient authority**: authority a program holds by virtue of who ran it rather than what it was handed — the condition of the confused deputy, whose "fundamental problem is that the compiler runs with authority stemming from two sources" ([Hardy 1988](http://cap-lore.com/CapTheory/ConfusedDeputy.html)).
- **declared scope**: the task's brief, read as a capability list — three sets with different rights (edit, never touch, scratch).
- **proof-carrying result**: a result that ships with a certificate a cheap checker verifies: "the untrusted code producer must supply with the code a safety proof that attests to the code's adherence to a previously defined safety policy" (Necula 1996).
- **enforcement point**: where the check runs — in the contributor's client (a hook, opt-in) or at the server (a protected branch, not skippable).
- **cost per call**: what the confinement adds to each command the task runs, which for an agent is every tool call.

### What the field calls it

| The task | The field's name | Anchor |
|---|---|---|
| holding a task's commands to declared paths | sandboxing by explicit allowlist, unprivileged | bubblewrap README 2026 |
| checking every access while it happens | complete mediation, the reference-monitor idea | Saltzer and Schroeder 1975 |
| granting no more than the job needs | least privilege | Saltzer and Schroeder 1975 |
| refusing what was not declared | fail-safe defaults; `default allow := false` | Saltzer and Schroeder 1975; OPA docs 2026 |
| the brief's path list as the authority | a capability list, ticket-oriented | Saltzer and Schroeder 1975; capsicum(4) 2026 |
| the result carrying its own check | proof-carrying code; proof objects checked independently | Necula 1996; Avigad et al. 2026 |
| where the check runs | enforcement point: client hook or server gate | pre-commit 2026; GitHub docs 2026 |

### The strands, as sub-questions

1. Which kernel confinement gives which guarantee, and at what cost per call? (namespaces and bubblewrap; seccomp-bpf; Landlock; gVisor; Firecracker microVMs; nsjail)
2. How does a declared scope become least privilege — capability lists against ambient authority, and what does the difference cost the tools being confined? (Saltzer and Schroeder; Capsicum; Cap'n Proto; the confused deputy)
3. What makes a result checkable rather than trusted — proof-carrying code, Lean proof objects replayed by `lake build`, a verified kernel? (Necula; Lake; Avigad et al.; seL4)
4. Where is the enforcement point for a template's rules — a local hook, the launcher, a CI gate, a policy engine? (pre-commit; GitHub protected branches; OPA; Cedar; Conftest)

### The five properties, and which strand decides each

| Property | The kind of question it is | Decided by | Anchor |
|---|---|---|---|
| P1 writes land only in the edit set and `.scratch/` | safety invariant over paths | filesystem confinement with read and write as separate rights | Landlock docs 2026; capsicum(4) 2026 |
| P2 the never-touch set stays readable, never writable | safety needing finer rights than "in or out of the sandbox" | per-access rights on paths that stay visible | Landlock docs 2026; bubblewrap README 2026 |
| P3 no ambient authority: nothing undeclared is reached | the deputy problem | authority handed as a list, not inherited from the caller | Hardy 1988; Cap'n Proto docs 2026 |
| P4 the task fails closed when the sandbox cannot be built | fail-safe defaults | the launcher's own behaviour; kernel prerequisites stated, not assumed | Saltzer and Schroeder 1975; Landlock docs 2026 |
| P5 the claim "the scope held" is checked outside the sandboxed process | proof-carrying | a record of the applied confinement, re-derived and re-run elsewhere | Necula 1996; Lake docs 2026; GitHub docs 2026 |

Cost per call is not a sixth property but the constraint on all five: the confinement runs before every command of every task, so its latency is multiplied by the number of tool calls a task makes.

## Literature review

Step 2: what the fetched sources say, strand by strand, in their own words where the wording is the evidence.

### Strand 1: sandboxes and their cost per call

The kernel offers four distinct enforcement layers, and they are not interchangeable. seccomp-bpf filters the system-call interface itself, but the kernel documentation denies it the sandbox's name: "System call filtering isn't a sandbox. It provides a clearly defined mechanism for minimizing the exposed kernel surface" — and the filter is blind to what the arguments point at, since "BPF programs may not dereference pointers" ([seccomp filter docs](https://docs.kernel.org/userspace-api/seccomp_filter.html)). Its cost statement is the layering trade: "additional filters may be layered on which will increase evaluation time, but allow for further decreasing the attack surface."

Namespaces are the next layer and bubblewrap is their unprivileged front end: it "always creates a new mount namespace", builds the visible filesystem with read-only and read-write bind mounts, and can unshare the network namespace to "only a loopback device"; it needs no privileges because it builds on user namespaces, and its setuid mode "has been removed" ([bubblewrap README](https://github.com/containers/bubblewrap)). Its authors' warning is the strand's recurring one: the tool constructs the sandbox, the caller defines the security model.

Landlock moves the check into the kernel and the policy into the hands of the process being confined: an unprivileged LSM whose rulesets a thread applies to itself, with read and write as separate access rights, TCP bind and connect restrictable since ABI version 4, restrictions that only ever narrow ("there is a limit of 16 layers of stacked rulesets"), and a topology limit — threads sandboxed with filesystem restrictions "cannot modify filesystem topology, whether via mount(2) or pivot_root(2)" ([Landlock docs](https://docs.kernel.org/userspace-api/landlock.html)). The same page argues the layering from first principles: user-space interposition "can lead to race conditions or inconsistent evaluations", and namespaces "are not designed for access-control and then miss useful features for such use case". Landlock must be present in the kernel (`CONFIG_SECURITY_LANDLOCK=y`, and `landlock` in `CONFIG_LSM`) — a prerequisite a launcher must check, not assume.

Above those sit the two heavy tiers. gVisor "interceptss application system calls and acts as the guest kernel, without the need for translation through virtualized hardware", trading "reduced application compatibility and higher per-system call overhead" for a "flexible resource footprint"; its ptrace platform "has high context switch overhead, so system call-heavy applications may pay a performance penalty" ([gVisor architecture guide](https://github.com/gvisor/gvisor/tree/master/g3doc), [platforms](https://github.com/gvisor/gvisor/blob/master/g3doc/architecture_guide/platforms.md)). Firecracker is a machine, priced as one: "Boot in <125ms. Create up to 150 microVMs per second per host", "<5 MiB overhead per VM", five emulated devices, a `jailer` companion — built at AWS for Lambda's density ([Firecracker](https://firecracker-microvm.github.io/)). nsjail is the composition tool between the tiers: "Linux process isolation tool using namespaces, resource limits, and seccomp-bpf syscall filters", with Kafel policies and three modes — LISTEN, RERUN, ONCE — that make its unit a fresh jailed process per command ([nsjail](https://github.com/google/nsjail)).

The practice closest to this issue is Anthropic's, and it states the cost ladder the other sources only imply. Their OS-level sandbox on Linux is bubblewrap: "reads are allowed, writes are allowed inside the workspace, but network is denied by default", which cut permission prompts by 84%; their environments ladder by "Isolation Overhead" — "Container spin-up / Low-latency native sandbox / Full VM boot" — and their reliability note is a design lesson: "The hypervisor, seccomp, and gVisor across our products have been dependable. Our custom allowlist proxy was the piece that failed." The per-command model is named outright: "a privileged process sits outside the sandbox deciding per-command whether to enforce it" ([how we contain Claude](https://www.anthropic.com/research/how-we-contain-claude), [beyond permission prompts](https://www.anthropic.com/research/claude-code-sandboxing)).

### Strand 2: capability lists and least privilege from a declared scope

The 1975 paper gives this issue its name and its shape. Least privilege is quoted above; fail-safe defaults is the brief's own grammar ("Edit only these paths" is permission, not exclusion); complete mediation is what a sandbox owes every access. The glossary's capability definition — the unforgeable ticket — is what a task's declared path list is, if anything enforces it: each entry names an object and confers a right ([Saltzer and Schroeder 1975](https://web.mit.edu/Saltzer/www/publications/protection/), [design principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)).

Capsicum shows the cost of taking that literally: it "makes file descriptors into capabilities", refinable so "a file descriptor returned by open(2) may be refined using cap_rights_limit(2) so that only read(2) and write(2) can be called, but not fchmod(2)" — but capability mode goes further than a path list can follow: "access to global OS namespaces (such as the file system and PID namespaces) is restricted; only explicitly delegated rights, referenced by memory mappings or file descriptors, may be used" ([capsicum(4)](https://man.freebsd.org/cgi/man.cgi?query=capsicum)). The agent's tools are unmodified binaries that address the world by path; they cannot live in capability mode.

The confused deputy is the failure a declared scope prevents, and its original case is almost this repository's: a privileged compiler invoked by an unprivileged user writes a billing file because its own authority, not the user's, named the target. "The capability both identifies the file and authorizes the compiler to write there" is the fix — hand the deputy the target instead of letting it use its own ([Hardy 1988](http://cap-lore.com/CapTheory/ConfusedDeputy.html)). Cap'n Proto's RPC page makes the same argument for object capabilities: references "both designate an object to call and confer permission to call it", and such patterns "tend to be much more adaptable than traditional ACL-based security, making it easy to keep security tight and avoid confused-deputy attacks" ([Cap'n Proto](https://capnproto.org/rpc.html)).

### Strand 3: proof-carrying results

The strand's founding idea splits producing from checking, and prices the split: "the untrusted code producer must supply with the code a safety proof that attests to the code's adherence to a previously defined safety policy", while the consumer "is able to use a simple and fast proof validator to check, with certainty, that the proof is valid", "all based on the intuition that proof checking is believed to be much easier than proof generation" — and the trust bottoms out in one place: "the code consumer need only trust one implementation of proof checking" (Necula 1996, [PLDI '96 paper](https://courses.grainger.illinois.edu/cs421/fa2010/papers/necula-pcc.pdf)).

Lean supplies the working instance of a checker that replays rather than trusts: theorem proving "focuses on the 'verification' aspect", requiring "that every claim is supported by a proof in a suitable axiomatic foundation", with "fully elaborated 'proof objects' that can be communicated to other systems and checked independently" ([Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)). Its build system makes the replay incremental and reproducible rather than a full re-run: a module is "the smallest unit of code visible to Lake's build system", a trace "is a piece of data (generally a hash) which is used to verify whether a given target is up-to-date", and the resolved revisions are saved "to `lake-manifest.json` to enable reproducibility" ([Lake](https://github.com/leanprover/lake)).

seL4 is the upper bound — enforcement itself proven: "a formal mathematical proof that it behaves exactly as specified", with "machine-checked mathematical proofs from high-level specifications to binary code" ([seL4](https://sel4.systems/), [verification](https://sel4.systems/Verification/)). It is cited here as a bound, not a candidate: nothing in this family's threat model needs a verified kernel, and no fetched source extends the result to a launcher's configuration of one.

### Strand 4: workflow enforcement for templates

The enforcement point decides whether a rule is advice or a gate. pre-commit runs in the client, pins its hooks — "pre-commit assumes that the value of `rev` is an immutable ref (such as a tag or SHA) and will cache based on that" — and is explicit that it is the fast half of a pair, recommending "pre-commit run --all-files as a CI step" ([pre-commit](https://pre-commit.com/)). The server half is the protected branch: "Required status checks must have a successful, skipped, or neutral status before collaborators can make changes to a protected branch", and a push that ignores the local rules entirely is refused at the remote — "remote: error: GH006: Protected branch update failed for refs/heads/main" ([GitHub docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).

Policy engines move the rules out of the program's code entirely. OPA describes the decoupling as the point — "decoupling policy from application logic", enforceable "in applications, proxies, Kubernetes, CI/CD pipelines, API gateways, and more" — and its idiom is this issue's fourth term: `default allow := false` ([OPA](https://www.openpolicyagent.org/), [docs](https://www.openpolicyagent.org/docs/latest/)). Cedar states the same separation — "Because Cedar policies are separate from application code, they can be independently authored, updated, analyzed, and audited" — adds a validator "to check that Cedar policies are consistent with a declared schema", and aims its analyzer at "proving that your security model is what you believe it is" ([Cedar](https://github.com/cedar-policy/cedar)). Conftest carries the idiom into CI against configuration files: "write tests against structured configuration data", with policies that "look for `deny`, `violation`, and `warn` rules" ([Conftest](https://www.conftest.dev/)).

## State of the art

Step 3: per strand, the best current method and its known limits.

### Strand 1: the mechanisms, what each holds, and what it costs

| Mechanism | What it holds | Cost, in the source's own words | What it leaves |
|---|---|---|---|
| seccomp-bpf | the system-call surface, inherited by children | "additional filters… will increase evaluation time" | "System call filtering isn't a sandbox"; arguments not dereferenced |
| bubblewrap + namespaces | the visible filesystem, the network, PIDs | none stated by the source; the practice calls this tier "low-latency native sandbox" | "not a complete, ready-made sandbox"; policy is the caller's arguments |
| Landlock | per-path read/write rights, TCP ports, in-kernel | no number in the source; the check is an LSM hook, not an interposer | kernel must be built and booted with it; 16 layers; no topology changes |
| gVisor | the whole guest kernel | "higher per-system call overhead"; ptrace has "high context switch overhead" | "reduced application compatibility" |
| Firecracker | a machine boundary | "Boot in <125ms", "<5 MiB overhead per VM" | a machine per task; five devices; a jailer to run it |
| nsjail | namespaces + rlimits + seccomp, per command | none stated; the model is a fresh jailed process per command | assembly required: the policy is still Kafel or arguments |

The strand's answer: only the first three rows are priced for a per-command launcher, and of those only Landlock separates read from write on paths that stay visible — which is P2, the property this repository's never-touch list needs. The two heavy tiers are priced for hostile tenants at density: Firecracker's own numbers are about how many microVMs fit on a host, not how few milliseconds a command costs.

### Strand 2: from a declared scope to least privilege

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Saltzer and Schroeder 1975 | the three principles the sandbox must satisfy, and the ticket/list distinction that makes a brief's path list a capability list | strongest, and fifty years old |
| upper bound | capsicum(4) 2026 | file descriptors as capabilities, rights refinable per descriptor — read without fchmod | strong, but capability mode forecloses path-addressed tools |
| limit | Hardy 1988 | the deputy's own authority is the vulnerability; hand it the target instead | the failure mode, not the mechanism |
| most adopted | Cap'n Proto 2026 | object capabilities in an RPC protocol; "much more adaptable than traditional ACL-based security" | the practice, in a different layer |

The strand's answer: the brief already *is* the capability list; the sandbox is the compiler from that list to confinement. A full capability model is not reachable — the tools are unmodified and address the filesystem by path — but the list-oriented half, an explicit allowlist consulted on every write, is exactly P1–P3 and costs one fork.

### Strand 3: results that carry their check

| Record | Holder | What it says | Grade |
|---|---|---|---|
| best evidence | Necula 1996 | checking is much easier than generation; one checker to trust | strongest |
| upper bound | seL4 2026 | enforcement proven from specification to binary | strongest, and far past the need |
| the working instance | Lake 2026; Avigad et al. 2026 | proofs replayed by a build whose traces say what is up to date; proof objects "checked independently" | the practice |
| limit | none found | no fetched source prices proof-carrying for a sandbox *configuration*; PCC certifies code against a safety policy, not a launcher's arguments against a brief | the known bound |

The strand's answer: the transferable idea is not the theorem but the split — the task produces, a small outside checker verifies, and the record of what was applied is the certificate. P5 needs a checkable artifact, not a proof.

### Strand 4: where the rule runs

| Record | Holder | What it says | grade |
|---|---|---|---|
| client | pre-commit 2026 | pinned, fast, per-contributor — and skippable by the same contributor | fast, not final |
| server | GitHub docs 2026 | required status checks and protected branches; `GH006` refuses the push | final |
| policy as data | OPA 2026; Cedar 2026 | `default allow := false`; policies decoupled, schema-validated, analyzable | the idiom |
| in CI | Conftest 2026 | `deny` rules run against structured configuration files | the practice |

The strand's answer: a template's rules need both halves — the launcher's per-command check in the client, and the same scope re-derived and re-run by CI on the server, which is what `checks/instance.py` already does for practices and `.github/workflows/checks.yml` already runs. The hook is convenience; the protected branch is the guarantee.

## Position

Step 4: what follows for the thing issue 9 names — a task sandbox built from the template — read as the specification of a small Rust launcher that reads a task's brief.

**What it should apply.**

1. **Compile the brief into an allowlist, deny by default.** The three sets in a task's "Decided" — edit, never touch, scratch — become the configuration; anything unlisted is read-only or invisible, and an empty list means an empty write set. This is fail-safe defaults rendered as code, the idiom Rego states as `default allow := false`.
2. **Run every command under bubblewrap.** The whole tree bound read-only; the edit set and `.scratch/` bound read-write; the network unshared to loopback only, so network is denied unless the brief declares it. This is Anthropic's shipped design — "reads are allowed, writes are allowed inside the workspace, but network is denied by default" — and it is the tier their own ladder prices at "low-latency native sandbox". P1 and P3 are settled by one fork per command.
3. **Add Landlock for the split namespaces cannot express.** The never-touch set must stay *readable* while the edit set is writable, and the agent's tools need the whole tree visible; Landlock's per-path read/write rights do that without hiding anything, checked in the kernel rather than by an interposer that "can lead to race conditions". P2 is Landlock's property.
4. **Cut the syscall surface with seccomp**, in the knowledge the kernel doc hands us: it "isn't a sandbox", it minimizes the exposed surface — mount, ptrace and their kin denied, filters inherited by children.
5. **Emit the applied confinement as data** — the actual paths, rights and namespace flags the launcher built — into the task's record. Then the result is proof-carrying in PCC's exact shape: the task produced it, and a small outside checker re-derives the scope from the same brief and compares, the way Lake's traces and `lake-manifest.json` let a build be verified rather than re-done. The delegator's acceptance check and CI's `unittest discover` are the two checkers already running.
6. **Fail closed and say so.** No user namespaces or no Landlock means no task, reported the way `checks/instance.py` reports a local-only practice rather than silently skipping it. P4 is the launcher's own behaviour, and it is the one property no mechanism in strand 1 supplies.

**What it should leave out.**

- **Firecracker and gVisor.** Priced for hostile tenants at density — "<125ms" boot and "<5 MiB" per machine, "higher per-system call overhead" per call — and this family's threat is a competent agent writing the wrong file, not a sandbox escape artist. The cost ladder has three rungs and this task needs the bottom one.
- **Capability mode.** Capsicum's capability mode "restricts" the very namespaces path-addressed tools live in; the launcher should take the ticket orientation of the capability idea and leave the capability model.
- **A verified kernel, and a theorem about the launcher.** seL4's results are "machine-checked mathematical proofs from high-level specifications to binary code" — proof effort belongs where the artifact *is* the claim. The launcher's brief-to-config compiler is small enough to test by the family's own oracle, S3: a test a program runs.
- **A running policy engine.** OPA as a service is a hop on every call. Keep only what travels: policy as data, decoupled from the launcher, schema-checked and `deny`-oriented, so the scope can be reviewed as a file and checked in CI without the launcher running at all.

**Named baseline:** `bwrap --ro-bind / / --bind <edit-set> <edit-set> --bind .scratch/.scratch --unshare-net --new-session <command>` — the plain bubblewrap invocation an hour of shell could build from a brief today; the launcher earns its keep only by adding P2 (Landlock's read/write split), P4 (failing closed) and P5 (the applied-config record) on top of it, at the same cost per call.

## Sources

Fetched 25 Nov. 2026; quoted text is verbatim from the page cited.

| Holder | URL | Kind |
|---|---|---|
| bubblewrap README | https://github.com/containers/bubblewrap | grey |
| Landlock UAPI | https://docs.kernel.org/userspace-api/landlock.html | grey, kernel documentation |
| seccomp filter UAPI | https://docs.kernel.org/userspace-api/seccomp_filter.html | grey, kernel documentation |
| gVisor architecture guide | https://github.com/gvisor/gvisor/tree/master/g3doc | grey |
| gVisor platforms | https://github.com/gvisor/gvisor/blob/master/g3doc/architecture_guide/platforms.md | grey |
| Firecracker | https://firecracker-microvm.github.io/ | grey |
| nsjail | https://github.com/google/nsjail | grey |
| Anthropic, how we contain Claude | https://www.anthropic.com/research/how-we-contain-claude | grey, engineering |
| Anthropic, beyond permission prompts | https://www.anthropic.com/research/claude-code-sandboxing | grey, engineering |
| Saltzer and Schroeder 1975, protection | https://web.mit.edu/Saltzer/www/publications/protection/ | academic |
| Saltzer and Schroeder 1975, design principles | https://web.mit.edu/Saltzer/www/publications/protection/Basic.html | academic |
| FreeBSD capsicum(4) | https://man.freebsd.org/cgi/man.cgi?query=capsicum | grey, OS documentation |
| Cap'n Proto, capabilities | https://capnproto.org/rpc.html | grey |
| Hardy 1988, the confused deputy | http://cap-lore.com/CapTheory/ConfusedDeputy.html | academic, author-hosted |
| Necula 1996, proof-carrying code | https://courses.grainger.illinois.edu/cs421/fa2010/papers/necula-pcc.pdf | academic (PLDI '96; sole author — the Necula and Lee version is POPL 1997) |
| Theorem Proving in Lean 4 | https://leanprover.github.io/theorem_proving_in_lean4/ | grey, textbook |
| Lake, the Lean 4 build system | https://github.com/leanprover/lake | grey |
| seL4 | https://sel4.systems/ | grey, verified results published |
| seL4 verification | https://sel4.systems/Verification/ | grey |
| pre-commit | https://pre-commit.com/ | grey |
| Open Policy Agent | https://www.openpolicyagent.org/ | grey |
| OPA documentation | https://www.openpolicyagent.org/docs/latest/ | grey |
| Cedar | https://github.com/cedar-policy/cedar | grey (cedar-policy.com was unreachable; the project's own README) |
| GitHub, about protected branches | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches | grey |
| Conftest | https://www.conftest.dev/ | grey |
