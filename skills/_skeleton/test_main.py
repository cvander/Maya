"""Tests for <skill-name>."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(fixture_dir=None, fmt="json", extra_args=None):
    cmd = [sys.executable, "-m", "skills.<skill_name>", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--inventory-dir", str(fixture_dir)])
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
        run = _run_skill(str(FIXTURES / "happy_path"))
        self.assertEqual(run["returncode"], 0)
        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)
        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_warn_golden(self):
        """Run against warn fixtures, verify findings present."""
        run = _run_skill(str(FIXTURES / "warn_case"))
        self.assertEqual(run["returncode"], 1)
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "warn")
        self.assertGreater(len(actual["findings"]), 0)


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


class TestEdgeCase(unittest.TestCase):
    def test_edge_case_no_crash(self):
        """Edge case fixtures should not crash the skill."""
        fixture_dir = str(FIXTURES / "edge_case")
        if not (FIXTURES / "edge_case").exists():
            self.skipTest("No edge_case fixtures")
        run = _run_skill(fixture_dir)
        self.assertIn(run["returncode"], (0, 1, 3))


if __name__ == "__main__":
    unittest.main()
