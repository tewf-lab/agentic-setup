"""The form of the review asked by brief.md: four files, each with its Shape line, 15 sources, a named baseline."""
import re
import unittest
from pathlib import Path

REVIEW = Path(__file__).resolve().parent / "review"
FILES = ["frame.md", "sources.md", "state-of-the-art.md", "baseline.md"]


class ReviewForm(unittest.TestCase):
    def test_each_file_has_its_shape_line(self):
        for name in FILES:
            text = (REVIEW / name).read_text(encoding="utf-8")
            self.assertIn("**Shape:**", text, name)

    def test_sources_hold_fifteen_urls(self):
        urls = set(re.findall(r"https?://[^\s)>\]]+", (REVIEW / "sources.md").read_text(encoding="utf-8")))
        self.assertGreaterEqual(len(urls), 15)

    def test_baseline_is_named(self):
        lines = (REVIEW / "baseline.md").read_text(encoding="utf-8").splitlines()
        self.assertTrue(any(line.startswith("**Baseline:**") for line in lines))


if __name__ == "__main__":
    unittest.main()
