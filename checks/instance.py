#!/usr/bin/env python3
"""One role: check one instance of the standard, so a family repository is told which of its practices hold.

The standard (standard.toml) states the practices, each a [practice.ID] table with its name and what it requires. An
instance answers in its agentic-setup.toml, one [ID] table per practice, holding the paths of the files that carry the
practice and the shell command test that proves it; where = "local" marks a test that cannot run in CI, and
waived = REASON admits the practice is not held yet, saying why. check() judges every practice of the standard against
that map, in the standard's order. Unmapped is an error. Waived is a warning whose message holds the reason. Otherwise
every path of files must exist under the instance root, an error naming the missing path, and the test runs in the
shell there with a timeout of 900 s, a non-zero exit an error holding "exit N" and the output's last lines. A table of
the map that names no practice of the standard is an error. A local-only test under ci=True is skipped and said in a
note, never judged.

Usage: python3 checks/instance.py [--standard PATH] [--instance PATH] [--map PATH] [--ci] [--list]
--list prints one line per practice (id, name, requires) and exits 0. Otherwise one line per result,
"kind practice message", exit 1 when any error, 0 otherwise. What cannot be read is said on stderr with exit 2, never
a traceback.

What it cannot do: it judges only what the map declares. A test that passes proves a practice no further than the test
looks; a table with no test of its own is taken on its files alone; and a hollow reason waves a practice through as a
warning, since the checker cannot weigh a reason, only repeat it.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

STANDARD = Path(__file__).resolve().parent.parent / "standard.toml"  # the standard beside checks/
MAP_NAME = "agentic-setup.toml"                                      # the file an instance answers the standard in
TIMEOUT = 900                                                        # seconds a test may run before it is failed
LAST_LINES = 5                                                       # output lines a failed test's error carries
LOCAL = "local"                                                      # the where of a test that cannot run in CI


@dataclass
class Result:
    """One judgement of one practice: its kind ('error', 'warning' or 'note'), the practice's id, what was found."""
    kind: str
    practice: str
    message: str


def load(path: Path, what: str) -> dict:
    """A TOML file as a dict; unread, or not TOML, becomes one ValueError naming the file and the reason."""
    try:
        with open(path, "rb") as handle:
            return tomllib.load(handle)
    except OSError as error:
        raise ValueError(f"{what} {path} cannot be read: {error}") from error
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"{what} {path} is not TOML: {error}") from error


def last_lines(*parts: str | None) -> str:
    """A test's output as its last lines on one, since a result prints as one line; none at all reads '(no output)'."""
    lines = [line.strip() for part in parts if part for line in part.splitlines() if line.strip()]
    return " | ".join(lines[-LAST_LINES:]) or "(no output)"


def run(pid: str, name: str, command: str, root: Path) -> list[Result]:
    """The practice's test command in the shell at the instance root; a non-zero exit, or the timeout, is an error
    holding the exit code, or the timeout, and the output's last lines."""
    try:
        done = subprocess.run(command, shell=True, cwd=str(root), capture_output=True, text=True,
                              errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired as stopped:
        tail = last_lines(stopped.stdout, stopped.stderr)
        return [Result("error", pid, f"{name}: test timed out after {TIMEOUT} s: {tail}")]
    if done.returncode == 0:
        return []
    tail = last_lines(done.stdout, done.stderr)
    return [Result("error", pid, f"{name}: test failed, exit {done.returncode}: {tail}")]


def files_of(entry: dict) -> list[str]:
    """The table's paths of files; one written bare, not in a list, is taken as the one path it names."""
    files = entry.get("files", [])
    return [files] if isinstance(files, str) else list(files)


def check(instance_root: Path, map_path: Path, standard_path: Path, ci: bool = False) -> list[Result]:
    """Every practice of the standard judged against the map, as the module docstring says, in the standard's order,
    then the map's tables that name no practice. A standard or a map that cannot be read raises ValueError."""
    root = Path(instance_root)
    practices = load(Path(standard_path), "the standard").get("practice", {})
    tables = load(Path(map_path), "the map")
    found: list[Result] = []
    for pid, practice in practices.items():
        name = practice.get("name", pid)
        entry = tables.get(pid)
        if not isinstance(entry, dict):
            found.append(Result("error", pid, f"{name}: not mapped — add a [{pid}] table to {Path(map_path).name}"))
        elif "waived" in entry:
            found.append(Result("warning", pid, f"{name}: waived — {entry['waived']}"))
        else:
            for file in files_of(entry):
                if not (root / file).exists():
                    found.append(Result("error", pid, f"{name}: missing {file} under {root}"))
            if entry.get("where") == LOCAL and ci:
                found.append(Result("note", pid, f"{name}: runs locally only, skipped in CI"))
            elif isinstance(entry.get("test"), str) and entry["test"].strip():
                found.extend(run(pid, name, entry["test"], root))
    for key, entry in tables.items():
        if isinstance(entry, dict) and key not in practices:
            found.append(Result("error", key, f"the map's [{key}] table names no practice of the standard"))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--standard", type=Path, default=STANDARD, help="the standard to check against")
    parser.add_argument("--instance", type=Path, default=Path(), help="the instance's root (default: this directory)")
    parser.add_argument("--map", type=Path, help="the instance's map (default: its agentic-setup.toml)")
    parser.add_argument("--ci", action="store_true", help="run as CI: a local-only test is skipped and said in a note")
    parser.add_argument("--list", action="store_true", help="print the standard's practices, one line each, and exit 0")
    args = parser.parse_args(argv)
    try:
        if args.list:
            for pid, practice in load(args.standard, "the standard").get("practice", {}).items():
                print(f"{pid} {practice.get('name', pid)} requires {practice.get('requires', '')}")
            return 0
        map_path = args.map if args.map is not None else args.instance / MAP_NAME
        found = check(args.instance, map_path, args.standard, ci=args.ci)
    except Exception as error:  # never a traceback, whatever the inputs hold
        print(f"instance: {error}", file=sys.stderr)
        return 2
    for result in found:
        print(f"{result.kind} {result.practice} {' '.join(str(result.message).split())}")
    return 1 if any(r.kind == "error" for r in found) else 0


if __name__ == "__main__":
    sys.exit(main())
