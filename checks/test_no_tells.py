"""Nothing in this public repository names the machine or the tools of one setup: the maintainer's rule for every public
repository (the work and what it needs to run, never how or where it was produced). The patterns are written so that
this file does not match itself. Run: python3 -m unittest checks/test_no_tells.py"""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TELLS = [r"Co-Authored-By: Cl[a]ude", r"Cl[a]ude-Session:", r"cl[a]ude\.ai/code", r"Generated with .{0,3}Cl[a]ude",
         r"Cl[a]ude Code", r"Cl[a]ude (Fable|Opus|Sonnet|Haiku)", r"l[o]calAI", r"l[o]calai", r"ask-l[o]cal",
         r"/h[o]me/h[a]mlil", r"[Oo]ll[a]ma", r"kimi-priv[a]te"]


class NoTells(unittest.TestCase):
    def test_no_tracked_file_names_the_setup(self):
        files = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True, check=True).stdout.split()
        hits = []
        for name in files:
            path = ROOT / name
            if not path.is_file() or path.suffix in {".svg", ".lock"}:
                continue
            text = path.read_text(errors="replace")
            hits += [f"{name}: {m.group(0)}" for pattern in TELLS for m in re.finditer(pattern, text)]
        self.assertEqual(hits, [], "\n".join(hits))


if __name__ == "__main__":
    unittest.main()
