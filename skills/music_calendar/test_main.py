"""Tests for music-calendar skill. stdlib unittest, golden-output pattern."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(fixture_dir=None, fmt="json", extra_args=None):
    """Run music-calendar as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.music_calendar", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--music-dir", str(fixture_dir)])
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}


def _strip_duration(d):
    """Remove metrics.duration_ms from a result dict for comparison."""
    copy = json.loads(json.dumps(d))
    if "metrics" in copy:
        copy["metrics"].pop("duration_ms", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_golden(self):
        """Run against happy_path fixtures, diff against expected.json."""
        run = _run_skill(
            str(FIXTURES / "happy_path"),
            extra_args=["--from", "2026-04-01", "--to", "2026-04-30"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)
        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_status_filter_confirmed(self):
        """Filter by confirmed status returns only confirmed events."""
        run = _run_skill(
            str(FIXTURES / "warn_case"),
            extra_args=["--from", "2026-04-01", "--to", "2026-04-30",
                         "--status", "confirmed"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        for event in actual["data"]["events"]:
            self.assertEqual(event["status"], "confirmed")
        self.assertEqual(len(actual["data"]["events"]), 1)

    def test_status_filter_tentative(self):
        """Filter by tentative status returns only tentative events."""
        run = _run_skill(
            str(FIXTURES / "warn_case"),
            extra_args=["--from", "2026-04-01", "--to", "2026-04-30",
                         "--status", "tentative"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        for event in actual["data"]["events"]:
            self.assertEqual(event["status"], "tentative")

    def test_date_range_filtering(self):
        """Events outside date range are excluded."""
        run = _run_skill(
            str(FIXTURES / "happy_path"),
            extra_args=["--from", "2026-04-19", "--to", "2026-04-22"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        # Only Midnight Sun on 2026-04-20 is in range
        self.assertEqual(len(actual["data"]["events"]), 1)
        self.assertEqual(actual["data"]["events"][0]["artist"], "Midnight Sun")

    def test_total_fees_calculated(self):
        """Total fees are correctly summed."""
        run = _run_skill(
            str(FIXTURES / "happy_path"),
            extra_args=["--from", "2026-04-01", "--to", "2026-04-30"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["data"]["total_fees"], 750)

    def test_empty_range(self):
        """Date range with no events returns empty list."""
        run = _run_skill(
            str(FIXTURES / "happy_path"),
            extra_args=["--from", "2026-01-01", "--to", "2026-01-31"],
        )
        self.assertEqual(run["returncode"], 0, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["data"]["events"], [])
        self.assertEqual(actual["data"]["total_fees"], 0)


class TestCodeQuality(unittest.TestCase):
    def test_no_print_calls(self):
        """No print() in skill code."""
        code = (Path(__file__).parent / "main.py").read_text()
        self.assertNotIn("print(", code)

    def test_no_direct_open(self):
        """No direct open() calls."""
        code = (Path(__file__).parent / "main.py").read_text()
        lines = [l for l in code.splitlines() if not l.strip().startswith("#")]
        joined = "\n".join(lines)
        self.assertNotIn("open(", joined)

    def test_no_fstring_in_log_events(self):
        """No f-strings in log.event() name arguments."""
        import re
        code = (Path(__file__).parent / "main.py").read_text()
        for m in re.finditer(r'log\.event\(f["\']', code):
            self.fail("f-string in log.event at position {pos}".format(pos=m.start()))

    def test_skill_md_matches_manifest(self):
        """SKILL.md frontmatter matches manifest.toml."""
        import tomllib
        manifest = tomllib.loads((Path(__file__).parent / "manifest.toml").read_text())["skill"]
        skill_md = (Path(__file__).parent / "SKILL.md").read_text()
        for field in ["name", "version", "description"]:
            self.assertIn(manifest[field], skill_md, "{field} mismatch".format(field=field))


if __name__ == "__main__":
    unittest.main()
