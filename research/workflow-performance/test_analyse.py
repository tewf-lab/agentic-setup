"""Tests of analyse.py over a fixture ledger written here, never the real logs/cost_ledger.jsonl.
Run: python3 -m unittest discover -s research/workflow-performance -p test_*.py"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # so analyse imports however the test is started

import analyse  # noqa: E402

# One JSON line per attempt, the shape delegator.ledger_row writes. The five jobs the figures must hold: j-1 passes on
# glm at attempt 1; j-2 fails on glm then passes on mistral at attempt 2, escalated from glm; j-3 is orphaned (its row
# holds only ts, week and job, as the orphan detector writes it); j-4 is a spec_error (the same keys plus repo); j-5 is
# stopped by the path guard, oracle not run. A sixth row, j-6, stops on the plan's quota, which is counted apart too.
LEDGER = """\
{"ts": "2026-11-24T10:00:00+0100", "week": "2026-W48", "job": "j-1", "attempt": 1, "repo": "reference-implementation", "class": "code", "backend": "glm", "tokens_in": 12000, "tokens_out": 2000, "cache_read": 30000, "usd": 0.0, "oracle": "pass", "path_guard": "ok", "escalated_from": null}
{"ts": "2026-11-24T11:00:00+0100", "week": "2026-W48", "job": "j-2", "attempt": 1, "repo": "reference-implementation", "class": "code", "backend": "glm", "tokens_in": 20000, "tokens_out": 4000, "cache_read": 50000, "usd": 0.0, "oracle": "fail", "path_guard": "ok", "escalated_from": null}
{"ts": "2026-11-24T11:20:00+0100", "week": "2026-W48", "job": "j-2", "attempt": 2, "repo": "reference-implementation", "class": "code", "backend": "mistral", "tokens_in": 8000, "tokens_out": 1500, "cache_read": 0, "usd": 0.04, "oracle": "pass", "path_guard": "ok", "escalated_from": "glm"}
{"ts": "2026-11-24T12:00:00+0100", "week": "2026-W48", "job": "j-3", "oracle": "orphaned"}
{"ts": "2026-11-24T12:30:00+0100", "week": "2026-W48", "job": "j-4", "repo": "reference-implementation", "oracle": "spec_error"}
{"ts": "2026-11-24T13:00:00+0100", "week": "2026-W48", "job": "j-5", "attempt": 1, "repo": "reference-implementation", "class": "research", "backend": "glm", "tokens_in": 5000, "tokens_out": 800, "cache_read": 1000, "usd": 0.0, "oracle": "not run", "path_guard": "outside the scope: notes.md", "escalated_from": null}
{"ts": "2026-11-24T14:00:00+0100", "week": "2026-W48", "job": "j-6", "attempt": 1, "repo": "reference-implementation", "class": "code", "backend": "glm", "tokens_in": 9000, "tokens_out": 900, "cache_read": 0, "usd": 0.0, "oracle": "quota", "path_guard": "ok", "escalated_from": null}
"""


def run(*argv: str) -> tuple[int, str]:
    """The command line over the fixture ledger, in a directory of its own, exactly as the README reads the real one."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "cost_ledger.jsonl"
        path.write_text(LEDGER, encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            code = analyse.main([str(path), *argv])
        return code, out.getvalue()


def report() -> dict:
    code, out = run()
    if code != 0:
        raise AssertionError(f"analyse exited {code} over the fixture ledger")
    return json.loads(out)


class Whole(unittest.TestCase):
    def test_seven_rows_hold_three_attempts_and_two_passes(self):
        rep = report()
        self.assertEqual((rep["rows"], rep["attempts"], rep["passes"]), (7, 3, 2))

    def test_orphaned_spec_error_and_quota_rows_are_counted_apart_never_as_attempts(self):
        self.assertEqual(report()["apart"], {"orphaned": 1, "spec_error": 1, "quota": 1})

    def test_the_guard_stopped_row_is_the_one_guard_violation(self):
        self.assertEqual(report()["guard_violations"], 1)

    def test_escalations_from_one_backend_to_another(self):
        self.assertEqual(report()["escalations"], {"glm->mistral": 1})


class Backends(unittest.TestCase):
    def test_glm_two_attempts_one_pass_and_one_guard_violation(self):
        f = report()["backends"]["glm"]
        self.assertEqual((f["attempts"], f["passes"]), (2, 1))
        self.assertAlmostEqual(f["first_attempt_pass_rate"], 0.5)   # j-1 passes its first, j-2 fails its first
        self.assertAlmostEqual(f["mean_tokens_in"], 16000.0)        # rows 1 and 2, never the guard-stopped row
        self.assertAlmostEqual(f["mean_tokens_out"], 3000.0)
        self.assertAlmostEqual(f["mean_cache_read"], 40000.0)
        self.assertAlmostEqual(f["usd"], 0.0)                        # a flat plan's rows cost 0 by construction
        self.assertAlmostEqual(f["usd_per_correct"], 0.0)
        self.assertEqual((f["escalations_in"], f["escalations_out"]), (0, 1))
        self.assertEqual(f["jobs_passed_on"], 1)
        self.assertEqual(f["guard_violations"], 1)

    def test_mistral_takes_the_escalation_and_passes(self):
        f = report()["backends"]["mistral"]
        self.assertEqual((f["attempts"], f["passes"]), (1, 1))
        self.assertAlmostEqual(f["first_attempt_pass_rate"], 1.0)   # j-2's first attempt there is its pass
        self.assertAlmostEqual(f["mean_tokens_in"], 8000.0)
        self.assertAlmostEqual(f["mean_tokens_out"], 1500.0)
        self.assertAlmostEqual(f["mean_cache_read"], 0.0)
        self.assertAlmostEqual(f["usd"], 0.04)
        self.assertAlmostEqual(f["usd_per_correct"], 0.04)
        self.assertEqual((f["escalations_in"], f["escalations_out"]), (1, 0))
        self.assertEqual(f["jobs_passed_on"], 1)
        self.assertEqual(f["guard_violations"], 0)


class Classes(unittest.TestCase):
    def test_code_three_attempts_two_passes(self):
        f = report()["classes"]["code"]
        self.assertEqual((f["attempts"], f["passes"]), (3, 2))
        self.assertAlmostEqual(f["first_attempt_pass_rate"], 0.5)   # j-2's quota stop sits in no denominator
        self.assertAlmostEqual(f["mean_tokens_in"], 40000 / 3)
        self.assertAlmostEqual(f["mean_tokens_out"], 2500.0)
        self.assertAlmostEqual(f["mean_cache_read"], 80000 / 3)
        self.assertAlmostEqual(f["usd"], 0.04)
        self.assertAlmostEqual(f["usd_per_correct"], 0.02)          # 0.04 usd over two correct answers
        self.assertEqual(f["escalations"], 1)
        self.assertEqual(f["guard_violations"], 0)
        self.assertEqual(f["passed_on"], {"glm": 1, "mistral": 1})

    def test_research_where_no_attempt_was_ever_judged(self):
        f = report()["classes"]["research"]
        self.assertEqual((f["attempts"], f["passes"]), (0, 0))
        self.assertIsNone(f["first_attempt_pass_rate"])   # None, never a 0 that would read as measured
        self.assertIsNone(f["mean_tokens_in"])
        self.assertIsNone(f["mean_tokens_out"])
        self.assertIsNone(f["mean_cache_read"])
        self.assertIsNone(f["usd_per_correct"])
        self.assertAlmostEqual(f["usd"], 0.0)
        self.assertEqual(f["escalations"], 0)
        self.assertEqual(f["guard_violations"], 1)        # the job the path guard stopped was research
        self.assertEqual(f["passed_on"], {})


class Jobs(unittest.TestCase):
    def test_the_rung_each_job_finally_passed_on(self):
        rep = report()
        self.assertEqual(rep["rungs_passed_on"], {"glm": 1, "mistral": 1})
        self.assertEqual(rep["jobs"]["j-1"]["passed_on"], "glm")
        self.assertEqual(rep["jobs"]["j-2"]["passed_on"], "mistral")

    def test_wall_time_between_first_and_last_rows_only_when_a_job_has_several(self):
        jobs = report()["jobs"]
        self.assertAlmostEqual(jobs["j-2"]["wall_seconds"], 1200.0)   # 11:00 to 11:20
        self.assertIsNone(jobs["j-1"]["wall_seconds"])
        self.assertIsNone(jobs["j-3"]["wall_seconds"])

    def test_how_each_job_ended(self):
        jobs = report()["jobs"]
        self.assertEqual([(j, jobs[j]["outcome"], jobs[j]["attempts"]) for j in sorted(jobs)],
                         [("j-1", "passed", 1), ("j-2", "passed", 2), ("j-3", "orphaned", 0),
                          ("j-4", "spec_error", 0), ("j-5", "failed", 0), ("j-6", "quota", 0)])

    def test_the_share_of_jobs_that_passed_failed_or_ended_orphaned(self):
        rep = report()
        self.assertEqual(rep["endings"], {"passed": 2, "orphaned": 1, "spec_error": 1, "quota": 1, "failed": 1})
        self.assertAlmostEqual(rep["shares"]["passed"], 0.5)    # over the four judged jobs, never over the two apart
        self.assertAlmostEqual(rep["shares"]["failed"], 0.25)
        self.assertAlmostEqual(rep["shares"]["orphaned"], 0.25)


class CommandLine(unittest.TestCase):
    def test_markdown_prints_tables_not_json(self):
        code, text = run("--markdown")
        self.assertEqual(code, 0)
        self.assertIn("| glm | 2 | 1 | 0.50 | 1 | 0 | 1 | 1 | 16,000 | 3,000 | 40,000 | 0.0000 | 0.0000 |", text)
        self.assertIn("| glm | mistral | 1 |", text)
        self.assertIn("| j-2 | passed | 2 | mistral | 1200 |", text)

    def test_a_ledger_that_cannot_be_read_exits_two(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = analyse.main(["/nowhere/cost_ledger.jsonl"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
