"""Tests for cost-analysis skill. stdlib unittest, golden-output pattern."""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(extra_args=None, fmt="json"):
    """Run cost-analysis as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.cost_analysis", "--format", fmt]
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
        """Run against happy_path fixture menu, diff against expected.json."""
        run = _run_skill(extra_args=[
            "--menu-file", str(FIXTURES / "happy_path" / "menu" / "current.md"),
            "--inventory-dir", str(FIXTURES / "happy_path" / "inventory"),
        ])
        self.assertEqual(run["returncode"], 1)  # warn status
        actual = json.loads(run["stdout"])

        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_warn_golden(self):
        """High pour cost items should trigger findings."""
        run = _run_skill(extra_args=[
            "--menu-file", str(FIXTURES / "warn_case" / "menu" / "current.md"),
            "--inventory-dir", str(FIXTURES / "warn_case" / "inventory"),
        ])
        self.assertEqual(run["returncode"], 1)
        actual = json.loads(run["stdout"])

        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))
        self.assertEqual(actual["status"], "warn")

        codes = [f["code"] for f in actual["findings"]]
        self.assertIn("HIGH_POUR_COST", codes)
        self.assertIn("LOW_MARGIN", codes)


class TestCategoryFilter(unittest.TestCase):
    def test_cocktails_only(self):
        """Category filter should limit results."""
        run = _run_skill(extra_args=[
            "--menu-file", str(FIXTURES / "happy_path" / "menu" / "current.md"),
            "--inventory-dir", str(FIXTURES / "happy_path" / "inventory"),
            "--category", "cocktails",
        ])
        self.assertIn(run["returncode"], (0, 1))
        actual = json.loads(run["stdout"])
        for item in actual["data"]["items"]:
            self.assertEqual(item["category"], "cocktails")


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
