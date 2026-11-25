"""Tests of task-sandbox, the launcher of issue 9 (research/sandbox/review.md, Position): a command runs under bubblewrap
with the whole tree read-only, only the task's declared scope and its scratch folder writable, the network closed unless
declared, and the applied confinement written as a record an outside checker can re-derive. It fails closed.
Version 1 is bubblewrap and the record; Landlock and seccomp come after.

    task-sandbox --root DIR --scope SCOPE.toml [--record FILE] -- COMMAND...

SCOPE.toml holds edit = [paths], never = [paths], scratch = ".scratch", network = false, paths relative to DIR.
Run: python3 -m unittest sandbox/test_launcher.py (builds with cargo first)."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BINARY = HERE / "target" / "release" / "task-sandbox"
CARGO = shutil.which("cargo") or str(Path.home() / ".cargo" / "bin" / "cargo")


def setUpModule():
    subprocess.run([CARGO, "build", "--quiet", "--release", "--manifest-path", str(HERE / "Cargo.toml")], check=True,
                   timeout=900)


class Launcher(unittest.TestCase):
    def setUp(self):
        cache = Path.home() / ".cache"          # not /tmp: inside the sandbox /tmp is a fresh, throwaway tmpfs
        cache.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=cache)
        self.root = Path(self.tmp.name) / "repo"
        (self.root / "src").mkdir(parents=True)
        (self.root / "secret").mkdir()
        (self.root / "src" / "a.py").write_text("old\n")
        (self.root / "README.md").write_text("readme\n")
        (self.root / "secret" / "key").write_text("k\n")
        self.scope = Path(self.tmp.name) / "scope.toml"
        self.scope.write_text('edit = ["src"]\nnever = ["secret"]\nscratch = ".scratch"\nnetwork = false\n')

    def tearDown(self):
        self.tmp.cleanup()

    def run_in(self, *command: str, record: Path | None = None, env: dict | None = None, scope: Path | None = None):
        argv = [str(BINARY), "--root", str(self.root), "--scope", str(scope or self.scope)]
        if record:
            argv += ["--record", str(record)]
        return subprocess.run(argv + ["--", *command], capture_output=True, text=True, timeout=60, env=env)

    def test_a_write_inside_the_edit_set_lands(self):
        done = self.run_in("sh", "-c", f"echo new > {self.root}/src/a.py")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((self.root / "src" / "a.py").read_text(), "new\n")

    def test_a_write_outside_the_scope_is_refused_and_nothing_changes(self):
        done = self.run_in("sh", "-c", f"echo changed > {self.root}/README.md")
        self.assertNotEqual(done.returncode, 0)
        self.assertEqual((self.root / "README.md").read_text(), "readme\n")

    def test_the_never_set_is_readable_and_not_writable(self):
        self.assertEqual(self.run_in("cat", f"{self.root}/secret/key").stdout, "k\n")
        self.assertNotEqual(self.run_in("sh", "-c", f"echo x > {self.root}/secret/key").returncode, 0)
        self.assertEqual((self.root / "secret" / "key").read_text(), "k\n")

    def test_the_scratch_folder_is_writable_and_created(self):
        self.assertEqual(self.run_in("sh", "-c", f"echo s > {self.root}/.scratch/s").returncode, 0)
        self.assertTrue((self.root / ".scratch" / "s").is_file())

    def test_the_network_is_closed_unless_declared(self):
        probe = "import socket; socket.create_connection(('1.1.1.1', 53), 2)"
        self.assertNotEqual(self.run_in("python3", "-c", probe).returncode, 0)

    def test_the_commands_exit_code_is_passed_through(self):
        self.assertEqual(self.run_in("sh", "-c", "exit 3").returncode, 3)

    def test_the_record_names_what_was_applied(self):
        record = Path(self.tmp.name) / "record.json"
        self.run_in("true", record=record)
        applied = json.loads(record.read_text())
        self.assertEqual(sorted(applied["writable"]), sorted([str(self.root / "src"), str(self.root / ".scratch")]))
        self.assertEqual(applied["read_only"], ["/"])
        self.assertFalse(applied["network"])
        self.assertEqual(applied["launcher"], "bubblewrap")
        self.assertIn("bwrap", applied["argv"][0])

    def test_a_scope_path_leaving_the_root_is_refused(self):
        bad = Path(self.tmp.name) / "bad.toml"
        bad.write_text('edit = ["../outside"]\nnever = []\nscratch = ".scratch"\nnetwork = false\n')
        marker = Path(self.tmp.name) / "ran"
        done = self.run_in("touch", str(marker), scope=bad)
        self.assertEqual(done.returncode, 2)
        self.assertFalse(marker.exists())

    def test_it_fails_closed_without_bubblewrap(self):
        marker = Path(self.tmp.name) / "ran"
        env = {**os.environ, "PATH": "/nonexistent"}
        done = self.run_in("/usr/bin/touch", str(marker), env=env)
        self.assertEqual(done.returncode, 2)
        self.assertIn("bubblewrap", done.stderr)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
