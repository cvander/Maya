"""Tests for compliance-check skill. stdlib unittest, golden-output pattern."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(
    fixture_dir: str | None = None,
    fmt: str = "json",
    date: str | None = None,
    days_ahead: int | None = None,
) -> dict:
    """Run compliance-check as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.compliance_check", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--compliance-dir", fixture_dir])
    if date:
        cmd.extend(["--date", date])
    if days_ahead is not None:
        cmd.extend(["--days-ahead", str(days_ahead)])
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


def _strip_duration(result_dict: dict) -> dict:
    """Remove metrics.duration_ms from a result dict for comparison."""
    copy = json.loads(json.dumps(result_dict))
    if "metrics" in copy:
        copy["metrics"].pop("duration_ms", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_golden(self):
        """Run against happy_path fixtures, diff against expected.json."""
        fixture_dir = str(FIXTURES / "happy_path" / "compliance")
        run = _run_skill(fixture_dir, date="2025-06-12")
        self.assertEqual(run["returncode"], 0,
                         "Expected exit 0, got {code}. stderr: {err}".format(
                             code=run["returncode"], err=run["stderr"]))

        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_warn_case_golden(self):
        """Run against warn_case fixtures, assert status warn and findings."""
        fixture_dir = str(FIXTURES / "warn_case" / "compliance")
        run = _run_skill(fixture_dir, date="2025-06-05")
        self.assertEqual(run["returncode"], 1,
                         "Expected exit 1, got {code}. stderr: {err}".format(
                             code=run["returncode"], err=run["stderr"]))

        actual = json.loads(run["stdout"])
        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))
        self.assertEqual(actual["status"], "warn")
        self.assertGreater(len(actual["findings"]), 0)


class TestCertExpired(unittest.TestCase):
    def test_expired_cert_is_fail_severity(self):
        """An expired cert should produce a CERT_EXPIRED finding with fail severity."""
        fixture_dir = str(FIXTURES / "warn_case" / "compliance")
        run = _run_skill(fixture_dir, date="2025-06-05")
        actual = json.loads(run["stdout"])
        expired = [f for f in actual["findings"] if f["code"] == "CERT_EXPIRED"]
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0]["severity"], "fail")


class TestDateFlag(unittest.TestCase):
    def test_invalid_date_returns_fail(self):
        """An invalid --date should produce a fail result."""
        fixture_dir = str(FIXTURES / "happy_path" / "compliance")
        run = _run_skill(fixture_dir, date="not-a-date")
        # The skill returns a fail result but runner still emits it
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "fail")


class TestCodeQuality(unittest.TestCase):
    """Grep-based checks: no print(), no open(), no f-string in log events."""

    _SKILL_CODE_FILES: list[Path] = []

    @classmethod
    def setUpClass(cls):
        skill_dir = REPO_ROOT / "skills" / "compliance_check"
        cls._SKILL_CODE_FILES = []
        for py in skill_dir.glob("*.py"):
            if py.name.startswith("test_"):
                continue
            cls._SKILL_CODE_FILES.append(py)

    def test_no_print_calls(self):
        """No print() calls in skill code (excluding tests)."""
        violations = []
        for py in self._SKILL_CODE_FILES:
            for i, line in enumerate(py.read_text().splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "print(" in line:
                    violations.append("{file}:{line}".format(file=py.name, line=i))
        self.assertEqual(violations, [], "print() found in: " + ", ".join(violations))

    def test_no_direct_open(self):
        """No direct open() calls in skill code (excluding tests)."""
        violations = []
        skill_dir = REPO_ROOT / "skills" / "compliance_check"
        for py in skill_dir.glob("*.py"):
            if py.name.startswith("test_"):
                continue
            for i, line in enumerate(py.read_text().splitlines(), 1):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "open(" in line:
                    violations.append("{file}:{line}".format(file=py.name, line=i))
        self.assertEqual(violations, [], "open() found in: " + ", ".join(violations))

    def test_no_fstring_in_log_events(self):
        """No f-strings in log.event() name arguments."""
        violations = []
        for py in self._SKILL_CODE_FILES:
            content = py.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                if "log.event(" in line and 'f"' in line or "f'" in line:
                    if "log.event(" in line:
                        violations.append("{file}:{line}".format(file=py.name, line=i))
        self.assertEqual(
            violations, [], "f-string in log.event: " + ", ".join(violations)
        )


if __name__ == "__main__":
    unittest.main()
