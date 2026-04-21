"""Tests for vendor-order-review skill. stdlib unittest, golden-output pattern."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(fixture_dir=None, fmt="json", extra_args=None):
    """Run vendor-order-review as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.vendor_order_review", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--inventory-dir", str(fixture_dir)])
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
        """No low stock items -> no orders needed."""
        fixture_dir = str(FIXTURES / "happy_path")
        input_file = str(FIXTURES / "happy_path" / "input.json")
        run = _run_skill(fixture_dir, extra_args=["--input-file", input_file])
        self.assertEqual(run["returncode"], 0)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_warn_case_golden(self):
        """Low stock items across 2 vendors -> orders generated."""
        fixture_dir = str(FIXTURES / "warn_case")
        input_file = str(FIXTURES / "warn_case" / "input.json")
        run = _run_skill(fixture_dir, extra_args=["--input-file", input_file])
        self.assertEqual(run["returncode"], 1)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))
        self.assertEqual(actual["status"], "warn")
        self.assertEqual(len(actual["findings"]), 3)


class TestNoInputFile(unittest.TestCase):
    def test_no_input_file_fails(self):
        """Missing --input-file should return fail status."""
        run = _run_skill()
        # Should return data error or fail
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "fail")


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
