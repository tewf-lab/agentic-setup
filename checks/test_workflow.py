"""The workflow graph and the standard cannot drift: every step of workflow.dot is a practice of standard.toml, and
every practice is a step, so a change to the workflow changes both, with their tests.
Run: python3 -m unittest checks/test_workflow.py"""
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Workflow(unittest.TestCase):
    def test_every_practice_is_a_step_of_the_graph_and_every_step_a_practice(self):
        practices = set(tomllib.loads((ROOT / "standard.toml").read_text())["practice"])
        steps = set(re.findall(r'label="(S\d+) ', (ROOT / "workflow.dot").read_text()))
        self.assertEqual(steps, practices)

    def test_the_drawing_is_rendered_from_its_source(self):
        self.assertTrue((ROOT / "workflow.svg").is_file())
        self.assertGreaterEqual((ROOT / "workflow.svg").stat().st_mtime, (ROOT / "workflow.dot").stat().st_mtime - 5)


if __name__ == "__main__":
    unittest.main()
