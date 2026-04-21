"""Tests for close-out skill. stdlib unittest, golden-output pattern."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(extra_args=None, fmt="json"):
    """Run close-out as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.close_out", "--format", fmt]
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


def _strip_dynamic(d):
    """Remove dynamic fields (duration_ms, output_file) for comparison."""
    copy = json.loads(json.dumps(d))
    copy["metrics"].pop("duration_ms", None)
    copy.get("data", {}).pop("output_file", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(dir=str(REPO_ROOT / "data"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_happy_path_golden(self):
        """Balanced register: variance within threshold."""
        run = _run_skill(extra_args=[
            "--date", "2026-04-10",
            "--cash-count", "850.00",
            "--card-total", "1200.00",
            "--expected", "2045.00",
            "--tip-total", "320.00",
            "--waste-items", "lime:5,beer:2",
            "--data-dir", self.tmpdir,
        ])
        self.assertEqual(run["returncode"], 0)
        actual = json.loads(run["stdout"])

        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_dynamic(actual), _strip_dynamic(expected))

        # Verify file was written
        output_file = Path(self.tmpdir) / "2026-04-10.md"
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("Close-Out: 2026-04-10", content)
        self.assertIn("$850.00", content)
        self.assertIn("lime", content)


class TestWarnCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(dir=str(REPO_ROOT / "data"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_warn_golden(self):
        """Cash short triggers CASH_SHORT finding."""
        run = _run_skill(extra_args=[
            "--date", "2026-04-10",
            "--cash-count", "825.00",
            "--card-total", "1200.00",
            "--expected", "2045.00",
            "--tip-total", "300.00",
            "--data-dir", self.tmpdir,
        ])
        self.assertEqual(run["returncode"], 1)
        actual = json.loads(run["stdout"])

        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_dynamic(actual), _strip_dynamic(expected))
        self.assertEqual(actual["status"], "warn")

        codes = [f["code"] for f in actual["findings"]]
        self.assertIn("CASH_SHORT", codes)


class TestMissingArgs(unittest.TestCase):
    def test_missing_required_args(self):
        """Missing required args should return fail status."""
        run = _run_skill(extra_args=["--date", "2026-04-10"])
        # The skill returns fail status but runner maps it to DATA_ERROR (3)
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "fail")


class TestWasteValidation(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(dir=str(REPO_ROOT / "data"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_invalid_waste_format(self):
        """Bad waste format should fail gracefully."""
        run = _run_skill(extra_args=[
            "--date", "2026-04-10",
            "--cash-count", "850.00",
            "--card-total", "1200.00",
            "--expected", "2045.00",
            "--waste-items", "badformat",
            "--data-dir", self.tmpdir,
        ])
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "fail")


class TestOverwriteGuard(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(dir=str(REPO_ROOT / "data"))

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_overwrite_blocked_without_force(self):
        """Running twice with same date should fail without --force."""
        args = [
            "--date", "2026-04-10",
            "--cash-count", "850.00",
            "--card-total", "1200.00",
            "--expected", "2045.00",
            "--data-dir", self.tmpdir,
        ]
        run1 = _run_skill(extra_args=args)
        self.assertEqual(run1["returncode"], 0)
        run2 = _run_skill(extra_args=args)
        actual = json.loads(run2["stdout"])
        self.assertEqual(actual["status"], "fail")
        self.assertIn("--force", actual["summary"])

    def test_overwrite_allowed_with_force(self):
        """Running twice with same date succeeds with --force."""
        args = [
            "--date", "2026-04-10",
            "--cash-count", "850.00",
            "--card-total", "1200.00",
            "--expected", "2045.00",
            "--data-dir", self.tmpdir,
        ]
        run1 = _run_skill(extra_args=args)
        self.assertEqual(run1["returncode"], 0)
        run2 = _run_skill(extra_args=args + ["--force"])
        self.assertEqual(run2["returncode"], 0)


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
