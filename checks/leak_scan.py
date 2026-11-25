#!/usr/bin/env python3
# Copied on 2026-11-25 from tewf-lab/agent-crossroads, scripts/leak_scan.py: this repository is public, and every push is
# scanned for what must never be in it.
"""Scan a rendered crossroads for what must never be in it: home paths, emails, keys.

  python3 scripts/leak_scan.py DIR      exit 1 on any hit

The private instance runs a stricter scan, with the names of its people, before it exports; this one holds no name, so
it can live in the template.
"""
import re
import sys
from pathlib import Path

PATTERNS = [r"/home/\w+", r"~/D[e]sktop", r"\$HOME/D[e]sktop", r"[\w.+-]+@[\w-]+\.[\w.-]+", r"sk-[A-Za-z0-9_-]{20,}",
            r"ghp_[A-Za-z0-9]{20,}", r"github_pat_\w{20,}", r"-----BEGIN [A-Z ]*PRIVATE KEY",
            r"(ANTHROPIC|ZAI|MISTRAL|OPENROUTER|OPENAI)_API_KEY\s*=\s*\S"]


def scan(root: Path) -> list[str]:
    hits = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            for p in PATTERNS:
                if re.search(p, line, re.I):
                    hits.append(f"{path.relative_to(root)}:{n}: {p}")
    return hits


if __name__ == "__main__":
    found = scan(Path(sys.argv[1]))
    print("\n".join(found) or "no leak")
    sys.exit(1 if found else 0)
