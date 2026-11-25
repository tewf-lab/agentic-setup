"""The data gathering of issue 9 (a task sandbox built from the template): the review has the four steps of a review,
names its baseline, covers each strand of the issue, and cites its sources. Run: python3 -m unittest research/sandbox/test_review.py"""
import re
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parent / "review.md"


class Review(unittest.TestCase):
    def setUp(self):
        self.text = REVIEW.read_text()

    def test_the_four_steps_and_the_baseline(self):
        for step in ("Frame", "Literature review", "State of the art", "Position"):
            self.assertRegex(self.text, rf"(?m)^##+ {step}\s*$", step)
        self.assertRegex(self.text, r"\*\*Named baseline:\*\* \S")

    def test_each_strand_of_the_issue_is_covered(self):
        for term in ("bubblewrap", "Landlock", "gVisor", "Firecracker", "capabilit", "least privilege", "proof-carrying",
                     "Lean", "pre-commit", "policy"):
            self.assertIn(term.lower(), self.text.lower(), term)

    def test_sources_are_cited(self):
        self.assertGreaterEqual(len(set(re.findall(r"https?://[^\s)>\]]+", self.text))), 12)


if __name__ == "__main__":
    unittest.main()
