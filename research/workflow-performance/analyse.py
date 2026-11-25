#!/usr/bin/env python3
"""One role: read the job ledger and say what the workflow itself measured, so jobs can be sent where they pass.

The ledger is the JSON lines of logs/cost_ledger.jsonl, one row per attempt (delegator.ledger_row), with the keys ts, job,
attempt, repo, class, backend, tokens_in, tokens_out, cache_read, usd, oracle, path_guard, escalated_from. A row counts as
an attempt only when its oracle is pass or fail, the convention of maestro/plan/estimators.py: a job that was orphaned
(its process died), spec_error (the acceptance command itself was broken) or stopped by the plan's quota says nothing
about the agent, so those rows are counted apart, never as attempts, and a row the path guard stopped (oracle not run)
is counted under guard violations and nowhere else.

Per backend and per class the report says: the attempts and the passes, the first-attempt pass rate over jobs (per
backend, of the jobs that have attempts there, the share whose first one there passed; per class, the same over each
job's attempts of that class), the rung each job finally passed on, the escalations from one backend to another (a row's
escalated_from names the rung that failed just before it), the guard violations, the mean tokens in, out and cached per
attempt, and the usd per correct answer, a group's whole usd over its passes, so a flat plan whose rows cost 0 by
construction shows 0 however often it fails. Over the jobs it says the wall time between the ts of a job's first and
last rows when it has several, and the share of jobs that passed, failed or ended orphaned: a job that ended spec_error
or quota is counted apart, not as a failure, exactly as the delegator refuses to bill a broken check or a spent plan to
the worker.

Usage: python3 analyse.py LEDGER [--markdown]
Prints the report as JSON, or as markdown tables with --markdown; exit 0 when the ledger is read, 2 when it is not.

What it cannot do: it sees only what the ledger recorded. GLM's rows carry no credits per call (glm_credits is null,
derived rather than read) and cost 0 usd by construction, so the study cannot weigh what a glm pass really spends, and
the steering seat's own tokens, the session that writes the specs and reads the envelopes, sit in no row of this ledger,
so the cost of steering itself is not measured.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ATTEMPTS = ("pass", "fail")                  # the oracle values that count as attempts
APART = ("orphaned", "spec_error", "quota")  # counted apart, never as attempts
GUARD_STOPPED = "not run"                    # what the delegator writes when the path guard trips
ENDINGS = ("passed", "orphaned", "spec_error", "quota", "failed")


def read_ledger(path: Path) -> list[dict]:
    """The ledger's rows, one JSON object a line; a line that is not JSON is said and left out, never guessed at."""
    rows = []
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                print(f"analyse: {path}:{number} is not a JSON line, left out", file=sys.stderr)
    return rows


def moment(text: object) -> datetime | None:
    """A row's ts as a clock reading, or None when the row has none a calendar can parse."""
    if not text:
        return None
    try:
        return datetime.fromisoformat(str(text).strip().replace("Z", "+00:00"))
    except ValueError:
        return None


def mean(values: list) -> float | None:
    """The mean of the figures the rows reported, a missing one counted 0; None over no attempts."""
    return sum(v or 0 for v in values) / len(values) if values else None


def figures(mine: list[dict]) -> dict:
    """What one group of rows says about itself: its attempts, passes, first-attempt pass rate over its jobs, guard
    violations, mean tokens per attempt, whole usd and usd per correct answer. A rate or mean no row supports is None,
    never a 0 that would read as measured."""
    attempts = sorted((r for r in mine if r.get("oracle") in ATTEMPTS),
                      key=lambda r: (r.get("attempt") or 0, str(r.get("ts") or "")))
    passes = sum(1 for r in attempts if r.get("oracle") == "pass")
    firsts: dict[str, dict] = {}
    for r in attempts:   # the rows sit in attempt order, so the first of each job kept is its first attempt
        firsts.setdefault(r.get("job"), r)
    usd = sum(float(r.get("usd") or 0.0) for r in attempts)
    return {"attempts": len(attempts),
            "passes": passes,
            "first_attempt_pass_rate": (sum(1 for r in firsts.values() if r.get("oracle") == "pass") / len(firsts)
                                        if firsts else None),
            "guard_violations": sum(1 for r in mine if r.get("path_guard") not in (None, "ok")),
            "mean_tokens_in": mean([r.get("tokens_in") for r in attempts]),
            "mean_tokens_out": mean([r.get("tokens_out") for r in attempts]),
            "mean_cache_read": mean([r.get("cache_read") for r in attempts]),
            "usd": usd,
            "usd_per_correct": usd / passes if passes else None}


def job_figures(mine: list[dict]) -> dict:
    """How one job ended, and what it took in time: the wall seconds between the ts of its first and last rows, only
    when it has several. A pass outranks everything (the delegator stops there); then orphaned, spec_error and quota,
    which are apart; a job the guard stopped, or whose attempts were all judged fail, is failed."""
    ordered = sorted(mine, key=lambda r: str(r.get("ts") or ""))
    oracles = {r.get("oracle") for r in ordered}
    attempts = [r for r in ordered if r.get("oracle") in ATTEMPTS]
    if "pass" in oracles:
        outcome = "passed"
        passed_on = next(r.get("backend") for r in reversed(attempts) if r.get("oracle") == "pass")
    elif "orphaned" in oracles:
        outcome, passed_on = "orphaned", None
    elif "spec_error" in oracles:
        outcome, passed_on = "spec_error", None
    elif "quota" in oracles:
        outcome, passed_on = "quota", None
    elif oracles & {"fail", GUARD_STOPPED}:
        outcome, passed_on = "failed", None
    else:
        outcome, passed_on = "not judged", None
    stamps = [t for t in (moment(r.get("ts")) for r in ordered) if t]
    return {"outcome": outcome, "attempts": len(attempts), "passed_on": passed_on,
            "wall_seconds": (stamps[-1] - stamps[0]).total_seconds() if len(stamps) > 1 else None}


def report(rows: list[dict], ledger: Path) -> dict:
    """Every figure of the study, from the ledger's rows: the whole, then per backend, per class, the escalations,
    the rung each job finally passed on, the jobs one by one, and how they ended."""
    jobs: dict[str, list[dict]] = {}
    for r in rows:
        jobs.setdefault(str(r.get("job")), []).append(r)
    job_view = {job: job_figures(mine) for job, mine in jobs.items()}
    job_class = {job: next((r.get("class") for r in sorted(mine, key=lambda r: str(r.get("ts") or "")) if r.get("class")), None)
                 for job, mine in jobs.items()}
    rungs_passed_on: dict[str, int] = {}
    for j in job_view.values():
        if j["passed_on"]:
            rungs_passed_on[j["passed_on"]] = rungs_passed_on.get(j["passed_on"], 0) + 1
    backends = {}
    for value in sorted({r.get("backend") for r in rows if r.get("backend")}):
        mine = [r for r in rows if r.get("backend") == value]
        entry = figures(mine)
        entry.update(escalations_in=sum(1 for r in mine if r.get("escalated_from")),
                     escalations_out=sum(1 for r in rows if r.get("escalated_from") == value),
                     jobs_passed_on=rungs_passed_on.get(value, 0))
        backends[value] = entry
    classes = {}
    for value in sorted({r.get("class") for r in rows if r.get("class")}):
        mine = [r for r in rows if r.get("class") == value]
        entry = figures(mine)
        passed_on: dict[str, int] = {}
        for job, j in job_view.items():
            if job_class.get(job) == value and j["passed_on"]:
                passed_on[j["passed_on"]] = passed_on.get(j["passed_on"], 0) + 1
        entry.update(escalations=sum(1 for r in mine if r.get("escalated_from")), passed_on=passed_on)
        classes[value] = entry
    pairs: dict[str, int] = {}
    for r in rows:
        prev = r.get("escalated_from")
        if prev:
            pair = f"{prev}->{r.get('backend')}"
            pairs[pair] = pairs.get(pair, 0) + 1
    endings = {end: sum(1 for j in job_view.values() if j["outcome"] == end) for end in ENDINGS}
    judged = endings["passed"] + endings["failed"] + endings["orphaned"]
    return {"ledger": str(ledger), "rows": len(rows),
            "attempts": sum(1 for r in rows if r.get("oracle") in ATTEMPTS),
            "passes": sum(1 for r in rows if r.get("oracle") == "pass"),
            "apart": {kind: sum(1 for r in rows if r.get("oracle") == kind) for kind in APART},
            "guard_violations": sum(1 for r in rows if r.get("path_guard") not in (None, "ok")),
            "backends": backends, "classes": classes, "escalations": pairs,
            "rungs_passed_on": rungs_passed_on, "jobs": job_view, "endings": endings,
            "shares": {end: endings[end] / judged if judged else None
                       for end in ("passed", "failed", "orphaned")}}


def _rate(value: float | None) -> str:
    return "-" if value is None else f"{value:.2f}"


def _tokens(value: float | None) -> str:
    return "-" if value is None else f"{value:,.0f}"


def _money(value: float | None) -> str:
    return "-" if value is None else f"{value:.4f}"


def markdown(rep: dict) -> str:
    """The report as markdown tables: one for the rungs, one for the classes, one for the moves between rungs, one for
    the jobs, one for how the jobs ended."""
    apart = rep["apart"]
    lines = [f"# The workflow, measured by its own ledger ({rep['ledger']})", "",
             f"{rep['rows']} rows, {rep['attempts']} attempts, {rep['passes']} passes; counted apart: "
             f"{apart['orphaned']} orphaned, {apart['spec_error']} spec_error, {apart['quota']} quota; "
             f"{rep['guard_violations']} guard violation(s).", "",
             "## Per backend", "",
             "| backend | attempts | passes | first-attempt pass rate | jobs passed on | escalations in |"
             " escalations out | guard violations | mean tokens in | mean tokens out | mean cached | usd |"
             " usd per correct |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, f in rep["backends"].items():
        lines.append(f"| {name} | {f['attempts']} | {f['passes']} | {_rate(f['first_attempt_pass_rate'])} | "
                     f"{f['jobs_passed_on']} | {f['escalations_in']} | {f['escalations_out']} | {f['guard_violations']} | "
                     f"{_tokens(f['mean_tokens_in'])} | {_tokens(f['mean_tokens_out'])} | {_tokens(f['mean_cache_read'])} | "
                     f"{_money(f['usd'])} | {_money(f['usd_per_correct'])} |")
    lines += ["", "## Per class", "",
              "| class | attempts | passes | first-attempt pass rate | finally passed on | escalations |"
              " guard violations | mean tokens in | mean tokens out | mean cached | usd | usd per correct |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, f in rep["classes"].items():
        rungs = ", ".join(f"{rung} {n}" for rung, n in sorted(f["passed_on"].items())) or "-"
        lines.append(f"| {name} | {f['attempts']} | {f['passes']} | {_rate(f['first_attempt_pass_rate'])} | {rungs} | "
                     f"{f['escalations']} | {f['guard_violations']} | {_tokens(f['mean_tokens_in'])} | "
                     f"{_tokens(f['mean_tokens_out'])} | {_tokens(f['mean_cache_read'])} | {_money(f['usd'])} | "
                     f"{_money(f['usd_per_correct'])} |")
    if rep["escalations"]:
        lines += ["", "## Escalations from one rung to another", "", "| from | to | attempts |", "|---|---|---|"]
        lines += [f"| {pair.split('->')[0]} | {pair.split('->')[1]} | {n} |"
                  for pair, n in sorted(rep["escalations"].items())]
    lines += ["", "## The jobs", "", "| job | outcome | attempts | finally passed on | wall s |", "|---|---|---|---|---|"]
    for job, j in rep["jobs"].items():
        wall = "-" if j["wall_seconds"] is None else f"{j['wall_seconds']:.0f}"
        lines.append(f"| {job} | {j['outcome']} | {j['attempts']} | {j['passed_on'] or '-'} | {wall} |")
    lines += ["", "## How the jobs ended", "", "| outcome | jobs | share |", "|---|---|---|"]
    for end, n in rep["endings"].items():
        lines.append(f"| {end} | {n} | {_rate(rep['shares'].get(end))} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("ledger", type=Path, help="the job ledger, one JSON line per attempt")
    parser.add_argument("--markdown", action="store_true", help="print the report as markdown tables instead of JSON")
    args = parser.parse_args(argv)
    try:
        rows = read_ledger(args.ledger)
    except OSError as error:
        print(f"analyse: {error}", file=sys.stderr)
        return 2
    rep = report(rows, args.ledger)
    print(markdown(rep) if args.markdown else json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
