"""The skeleton of a family repository, as Tewf/ai-augmented-agents has it: a README that states the standard and how an
implementation is checked, a changelog, a checks config extending reader-ergonomics, and a CI that runs both the
standard's checks and this repository's tests. Nothing of one machine in it: the repository may become public.
Run: python3 -m unittest checks/test_skeleton.py"""
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Skeleton(unittest.TestCase):
    def test_the_readme_states_the_standard_and_the_instance_check(self):
        text = (ROOT / "README.md").read_text()
        self.assertRegex(text, r"\*\*Shape:\*\* \[[^\]]+\]\([^)]*readme-and-folder\.md\)")
        for practice in tomllib.loads((ROOT / "standard.toml").read_text())["practice"]:
            self.assertIn(practice, text)
        for needed in ("checks/instance.py", "agentic-setup.toml", "localAI", "research/architecture", "research/sandbox"):
            self.assertIn(needed, text)

    def test_no_path_of_one_machine(self):
        for name in ("README.md", "CHANGELOG.md", "checks/config.toml", ".github/workflows/checks.yml"):
            self.assertIsNone(re.search(r"/h[o]me/|~/D[e]sktop|\bD[e]sktop/", (ROOT / name).read_text()), name)

    def test_the_changelog_and_the_checks_config(self):
        self.assertIn("Unreleased", (ROOT / "CHANGELOG.md").read_text())
        self.assertEqual(tomllib.loads((ROOT / "checks" / "config.toml").read_text()).get("extends"), "reader-ergonomics")

    def test_the_ci_runs_the_standard_and_the_tests(self):
        ci = (ROOT / ".github" / "workflows" / "checks.yml").read_text()
        for needed in ("Tewf/reader-ergonomics", "python-version", "unittest discover"):
            self.assertIn(needed, ci)


if __name__ == "__main__":
    unittest.main()
