"""Tests for schedule-draft skill."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(fixture_dir=None, fmt="json", extra_args=None):
    cmd = [sys.executable, "-m", "skills.schedule_draft", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--schedule-dir", str(fixture_dir)])
    if extra_args:
        cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}


def _strip_duration(d):
    copy = json.loads(json.dumps(d))
    copy["metrics"].pop("duration_ms", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_golden(self):
        """Run against happy_path fixtures, diff against expected.json."""
        run = _run_skill(str(FIXTURES / "happy_path"), extra_args=["--week-of", "2027-01-04"])
        self.assertEqual(run["returncode"], 1, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)
        self.assertEqual(_strip_duration(actual), _strip_duration(expected))

    def test_has_shifts(self):
        """Draft generates at least one shift."""
        run = _run_skill(str(FIXTURES / "happy_path"), extra_args=["--week-of", "2027-01-04"])
        actual = json.loads(run["stdout"])
        self.assertGreater(len(actual["data"]["shifts"]), 0)

    def test_overtime_flagged(self):
        """Draft flags overtime for shifts >8h."""
        run = _run_skill(str(FIXTURES / "happy_path"), extra_args=["--week-of", "2027-01-04"])
        actual = json.loads(run["stdout"])
        overtime_findings = [f for f in actual["findings"] if f["code"] == "OVERTIME_RISK"]
        self.assertGreater(len(overtime_findings), 0)


class TestWarnCase(unittest.TestCase):
    def test_warn_golden(self):
        """Warn case includes MISSING_CERT findings."""
        run = _run_skill(str(FIXTURES / "warn_case"), extra_args=["--week-of", "2027-01-04"])
        self.assertEqual(run["returncode"], 1, "stderr: " + run["stderr"])
        actual = json.loads(run["stdout"])
        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)
        self.assertEqual(_strip_duration(actual), _strip_duration(expected))

    def test_missing_cert_flagged(self):
        """Warn case flags bartender without RBS cert."""
        run = _run_skill(str(FIXTURES / "warn_case"), extra_args=["--week-of", "2027-01-04"])
        actual = json.loads(run["stdout"])
        cert_findings = [f for f in actual["findings"] if f["code"] == "MISSING_CERT"]
        self.assertGreater(len(cert_findings), 0)


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
