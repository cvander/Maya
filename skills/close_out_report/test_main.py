"""Tests for close-out-report skill. stdlib unittest, golden-output pattern."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(extra_args=None, fmt="json"):
    """Run close-out-report as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.close_out_report", "--format", fmt]
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def _strip_duration(d):
    """Remove metrics.duration_ms for comparison."""
    copy = json.loads(json.dumps(d))
    copy["metrics"].pop("duration_ms", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_golden(self):
        """Aggregate 3 days of close-out data."""
        fixture_dir = str(FIXTURES / "happy_path")
        run = _run_skill(extra_args=[
            "--data-dir", fixture_dir,
            "--from", "2026-04-08",
            "--to", "2026-04-10",
        ])
        self.assertEqual(run["returncode"], 0)
        actual = json.loads(run["stdout"])

        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))

    def test_date_range_filter(self):
        """Filtering by date range should reduce results."""
        fixture_dir = str(FIXTURES / "happy_path")
        run = _run_skill(extra_args=[
            "--data-dir", fixture_dir,
            "--from", "2026-04-09",
            "--to", "2026-04-09",
        ])
        self.assertEqual(run["returncode"], 0)
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["data"]["days"], 1)


class TestNoData(unittest.TestCase):
    def test_empty_dir(self):
        """Empty data dir should return ok with 0 days."""
        import tempfile
        import shutil
        tmpdir = tempfile.mkdtemp()
        try:
            run = _run_skill(extra_args=["--data-dir", tmpdir])
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["data"]["days"], 0)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestCodeQuality(unittest.TestCase):
    def test_no_print_calls(self):
        """No print() in skill code."""
        code = (Path(__file__).parent / "main.py").read_text()
        self.assertNotIn("print(", code)

    def test_no_direct_open(self):
        """No direct open() calls in skill code."""
        code = (Path(__file__).parent / "main.py").read_text()
        lines = [l for l in code.splitlines() if not l.strip().startswith("#")]
        joined = "\n".join(lines)
        self.assertNotIn("open(", joined)

    def test_no_fstring_in_log_events(self):
        """No f-strings in log.event() name arguments."""
        code = (Path(__file__).parent / "main.py").read_text()
        for m in re.finditer(r'log\.event\(f["\']', code):
            self.fail(
                "f-string in log.event at position {pos}".format(pos=m.start())
            )

    def test_skill_md_matches_manifest(self):
        """SKILL.md frontmatter matches manifest.toml."""
        import tomllib
        manifest = tomllib.loads(
            (Path(__file__).parent / "manifest.toml").read_text()
        )["skill"]
        skill_md = (Path(__file__).parent / "SKILL.md").read_text()
        for field in ["name", "version", "description"]:
            self.assertIn(
                manifest[field], skill_md,
                "{field} mismatch".format(field=field),
            )


if __name__ == "__main__":
    unittest.main()
