"""Tests of checks/instance.py: an implementation is checked against this repository's standard. An instance maps each
practice of standard.toml to its files and its test command in agentic-setup.toml; the checker fails when a practice
is unmapped, a mapped file is missing, or a test command fails. Run: python3 -m unittest checks/test_instance.py"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import instance  # noqa: E402

STANDARD = """[practice.S1]
name = "gate"
requires = "a gate"
[practice.S2]
name = "ledger"
requires = "a ledger"
"""


class Fixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.t = Path(self.tmp.name)
        self.standard = self.t / "standard.toml"
        self.standard.write_text(STANDARD)
        self.inst = self.t / "inst"
        self.inst.mkdir()
        (self.inst / "gate.py").write_text("x = 1\n")
        (self.inst / "ledger.py").write_text("x = 1\n")

    def tearDown(self):
        self.tmp.cleanup()

    def map(self, text: str) -> Path:
        path = self.inst / "agentic-setup.toml"
        path.write_text(text)
        return path

    def results(self, text: str, ci: bool = False):
        return instance.check(self.inst, self.map(text), self.standard, ci=ci)


GOOD = """[S1]
files = ["gate.py"]
test = "python3 -c 'pass'"
[S2]
files = ["ledger.py"]
test = "python3 -c 'pass'"
"""


class Check(Fixture):
    def test_a_complete_instance_passes(self):
        self.assertEqual([r for r in self.results(GOOD) if r.kind == "error"], [])

    def test_an_unmapped_practice_is_an_error(self):
        found = self.results(GOOD.split("[S2]")[0])
        self.assertTrue(any(r.kind == "error" and r.practice == "S2" and "not mapped" in r.message for r in found))

    def test_a_waived_practice_names_its_reason_and_is_a_warning(self):
        found = self.results(GOOD.split("[S2]")[0] + '[S2]\nwaived = "no ledger yet: issue 12"\n')
        self.assertTrue(any(r.kind == "warning" and r.practice == "S2" and "issue 12" in r.message for r in found))
        self.assertFalse(any(r.kind == "error" for r in found))

    def test_a_missing_file_is_an_error(self):
        found = self.results(GOOD.replace("ledger.py", "gone.py"))
        self.assertTrue(any(r.kind == "error" and r.practice == "S2" and "gone.py" in r.message for r in found))

    def test_a_failing_test_is_an_error(self):
        found = self.results(GOOD.replace("python3 -c 'pass'", "python3 -c 'raise SystemExit(1)'", 1))
        self.assertTrue(any(r.kind == "error" and r.practice == "S1" and "exit 1" in r.message for r in found))

    def test_a_local_only_test_is_skipped_in_ci_and_said_so(self):
        text = ('[S1]\nfiles = ["gate.py"]\ntest = "python3 -c \'pass\'"\n'
                '[S2]\nwhere = "local"\nfiles = ["ledger.py"]\ntest = "python3 -c \'raise SystemExit(1)\'"\n')
        found = self.results(text, ci=True)
        self.assertFalse(any(r.kind == "error" and r.practice == "S2" for r in found))
        self.assertTrue(any(r.kind == "note" and r.practice == "S2" and "local" in r.message for r in found))
        self.assertTrue(any(r.kind == "error" and r.practice == "S2" for r in self.results(text, ci=False)))

    def test_an_unknown_practice_in_the_map_is_an_error(self):
        found = self.results(GOOD + '[S9]\nfiles = ["gate.py"]\ntest = "true"\n')
        self.assertTrue(any(r.kind == "error" and r.practice == "S9" for r in found))


class Program(unittest.TestCase):
    def test_the_real_standard_loads_and_the_command_answers(self):
        done = subprocess.run([sys.executable, str(HERE / "instance.py"), "--standard", str(HERE.parent / "standard.toml"),
                               "--list"], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        for practice in ("S1", "S3", "S8", "S9"):
            self.assertIn(practice, done.stdout)


if __name__ == "__main__":
    unittest.main()
