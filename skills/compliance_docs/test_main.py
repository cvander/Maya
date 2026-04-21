"""Tests for compliance-docs skill. stdlib unittest, golden-output pattern."""

import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(
    fixture_dir: str | None = None,
    fmt: str = "json",
) -> dict:
    """Run compliance-docs as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.compliance_docs", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--compliance-dir", fixture_dir])
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


def _strip_volatile(result_dict: dict) -> dict:
    """Remove volatile fields (metrics, last_modified) for comparison."""
    copy = json.loads(json.dumps(result_dict))
    copy.pop("metrics", None)
    # Strip last_modified from docs entries (depends on file mtime)
    for doc in copy.get("data", {}).get("docs", []):
        doc.pop("last_modified", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_structure(self):
        """Run against happy_path fixtures, verify all docs ok."""
        fixture_dir = str(FIXTURES / "happy_path" / "compliance")
        run = _run_skill(fixture_dir)
        self.assertEqual(run["returncode"], 0,
                         "Expected exit 0, got {code}. stderr: {err}".format(
                             code=run["returncode"], err=run["stderr"]))

        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        # Compare structural fields (not mtime-dependent)
        self.assertEqual(actual["skill"], expected["skill"])
        self.assertEqual(actual["status"], expected["status"])
        self.assertEqual(actual["summary"], expected["summary"])
        self.assertEqual(actual["data"]["docs_checked"], expected["data"]["docs_checked"])
        self.assertEqual(actual["data"]["docs_present"], expected["data"]["docs_present"])
        self.assertEqual(actual["data"]["docs_missing"], expected["data"]["docs_missing"])
        self.assertEqual(actual["findings"], expected["findings"])


class TestWarnCase(unittest.TestCase):
    def test_warn_case_structure(self):
        """Run against warn_case fixtures, assert DOC_MISSING and DOC_EMPTY."""
        fixture_dir = str(FIXTURES / "warn_case" / "compliance")
        run = _run_skill(fixture_dir)
        self.assertEqual(run["returncode"], 1,
                         "Expected exit 1, got {code}. stderr: {err}".format(
                             code=run["returncode"], err=run["stderr"]))

        actual = json.loads(run["stdout"])
        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(actual["status"], expected["status"])
        self.assertEqual(actual["data"]["docs_checked"], expected["data"]["docs_checked"])
        self.assertEqual(actual["data"]["docs_present"], expected["data"]["docs_present"])
        self.assertEqual(actual["data"]["docs_missing"], expected["data"]["docs_missing"])

        # Verify expected finding codes are present
        actual_codes = sorted([f["code"] for f in actual["findings"]])
        self.assertEqual(actual_codes, sorted(expected["expected_codes"]))

    def test_missing_doc_is_identified(self):
        """incidents.md is missing in warn_case, should produce DOC_MISSING."""
        fixture_dir = str(FIXTURES / "warn_case" / "compliance")
        run = _run_skill(fixture_dir)
        actual = json.loads(run["stdout"])
        missing = [f for f in actual["findings"] if f["code"] == "DOC_MISSING"]
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["subject"], "incidents.md")

    def test_empty_doc_is_identified(self):
        """pest-log.md is empty in warn_case, should produce DOC_EMPTY."""
        fixture_dir = str(FIXTURES / "warn_case" / "compliance")
        run = _run_skill(fixture_dir)
        actual = json.loads(run["stdout"])
        empty = [f for f in actual["findings"] if f["code"] == "DOC_EMPTY"]
        self.assertEqual(len(empty), 1)
        self.assertEqual(empty[0]["subject"], "pest-log.md")


class TestStaleDetection(unittest.TestCase):
    def test_stale_doc_detected(self):
        """A file with old mtime should produce DOC_STALE finding."""
        import tempfile
        import shutil

        # Create a temporary fixture with an old file
        with tempfile.TemporaryDirectory() as tmpdir:
            comp_dir = Path(tmpdir) / "compliance"
            permits_dir = Path(tmpdir) / "permits"
            comp_dir.mkdir()
            permits_dir.mkdir()

            # Write all expected docs
            for fname in ["staff-certs.md", "cooler-temps.md", "pest-log.md", "incidents.md"]:
                src = FIXTURES / "happy_path" / "compliance" / fname
                dst = comp_dir / fname
                shutil.copy2(src, dst)
            shutil.copy2(
                FIXTURES / "happy_path" / "permits" / "README.md",
                permits_dir / "README.md",
            )

            # Make staff-certs.md appear stale (60 days old)
            stale_file = comp_dir / "staff-certs.md"
            old_time = time.time() - (60 * 86400)
            os.utime(str(stale_file), (old_time, old_time))

            run = _run_skill(str(comp_dir))
            actual = json.loads(run["stdout"])
            stale = [f for f in actual["findings"] if f["code"] == "DOC_STALE"]
            self.assertEqual(len(stale), 1)
            self.assertEqual(stale[0]["subject"], "staff-certs.md")


class TestCodeQuality(unittest.TestCase):
    """Grep-based checks: no print(), no open(), no f-string in log events."""

    _SKILL_CODE_FILES: list[Path] = []

    @classmethod
    def setUpClass(cls):
        skill_dir = REPO_ROOT / "skills" / "compliance_docs"
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
        skill_dir = REPO_ROOT / "skills" / "compliance_docs"
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
