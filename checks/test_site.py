"""The site of this repository, published by GitHub Pages as the families publish theirs (Tewf/ai-augmented-agents):
Quarto at a pinned version, the standard's stylesheet at a pinned commit, the concept's pages rendered and the checks,
the sandbox's code and generated research output left out. Run: python3 -m unittest checks/test_site.py"""
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Site(unittest.TestCase):
    def test_the_quarto_project_is_the_concepts(self):
        text = (ROOT / "_quarto.yml").read_text()
        for needed in ("type: website", "output-dir: _site", "https://tewf-lab.github.io/agentic-setup/",
                       "https://github.com/tewf-lab/agentic-setup", '"!checks/"', '"!sandbox/"'):
            self.assertIn(needed, text)
        self.assertTrue((ROOT / "index.qmd").is_file() or (ROOT / "index.md").is_file())

    def test_the_pages_workflow_is_the_families_pinned(self):
        text = (ROOT / ".github" / "workflows" / "pages.yml").read_text()
        for needed in ("actions/deploy-pages@v4", "actions/upload-pages-artifact@v3", "quarto-dev/quarto-actions/setup@v2",
                       "version: 1.8.26", "65e42472e2d4cbfd994c2a86e95a47e5dc7301ca", "branches: [main]", "pages: write"):
            self.assertIn(needed, text)

    def test_the_rendered_site_stays_out_of_git(self):
        ignored = (ROOT / ".gitignore").read_text()
        self.assertIn("_site/", ignored)
        self.assertIn(".quarto/", ignored)

    @unittest.skipUnless(shutil.which("quarto"), "quarto is not installed here")
    def test_it_renders(self):
        done = subprocess.run(["quarto", "render", "--quiet"], cwd=ROOT, capture_output=True, text=True, timeout=600)
        self.assertEqual(done.returncode, 0, done.stderr[-2000:])
        self.assertTrue((ROOT / "_site" / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
