"""Tests for eighty-six skill. stdlib unittest, golden-output pattern."""

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


def _run_skill(
    data_dir: str | None = None,
    fmt: str = "json",
    extra_args: list[str] | None = None,
) -> dict:
    """Run eighty-six as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.eighty_six", "--format", fmt]
    if data_dir:
        cmd.extend(["--data-dir", data_dir])
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


def _strip_duration(result_dict: dict) -> dict:
    """Remove metrics.duration_ms from a result dict for comparison."""
    copy = json.loads(json.dumps(result_dict))
    if "metrics" in copy:
        copy["metrics"].pop("duration_ms", None)
    return copy


class TestHappyPath(unittest.TestCase):
    def test_happy_path_golden(self):
        """Run --list against empty 86 list, diff against expected.json."""
        fixture_dir = str(FIXTURES / "happy_path")
        run = _run_skill(data_dir=fixture_dir)
        self.assertEqual(run["returncode"], 0)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestWarnCase(unittest.TestCase):
    def test_warn_golden(self):
        """Run --list against 86 list with 2 items, verify findings."""
        fixture_dir = str(FIXTURES / "warn_case")
        run = _run_skill(data_dir=fixture_dir)
        self.assertEqual(run["returncode"], 1)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "warn_case" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))
        self.assertEqual(actual["status"], "warn")
        self.assertEqual(len(actual["findings"]), 2)


class TestAddItem(unittest.TestCase):
    def test_add_creates_file_and_entry(self):
        """--add creates current.md with the item if file does not exist."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=[
                    "--add", "Starlight Lager",
                    "--reason", "Keg blew",
                    "--reported-by", "Taylor",
                ],
            )
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["status"], "ok")
            self.assertEqual(actual["data"]["item"], "Starlight Lager")
            self.assertEqual(actual["data"]["action"], "add")
            self.assertIn("beer", actual["data"]["category"])

            # Verify file was written
            written = Path(tmpdir) / "current.md"
            self.assertTrue(written.exists())
            content = written.read_text()
            self.assertIn("Starlight Lager", content)
            self.assertIn("Keg blew", content)
            self.assertIn("Taylor", content)

    def test_add_to_existing_list(self):
        """--add appends to existing 86 list."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            # Copy warn_case fixture
            shutil.copy(
                FIXTURES / "warn_case" / "current.md",
                Path(tmpdir) / "current.md",
            )
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=[
                    "--add", "Crimson Merlot",
                    "--reason", "Last bottle sold",
                    "--reported-by", "Riley",
                ],
            )
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["data"]["item"], "Crimson Merlot")

            # Verify 3 items now in file
            content = (Path(tmpdir) / "current.md").read_text()
            self.assertIn("Golden Horizon IPA", content)
            self.assertIn("Midnight Velvet Bourbon", content)
            self.assertIn("Crimson Merlot", content)

    def test_add_duplicate_warns(self):
        """--add of existing item returns warn status."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            shutil.copy(
                FIXTURES / "warn_case" / "current.md",
                Path(tmpdir) / "current.md",
            )
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=[
                    "--add", "Golden Horizon IPA",
                    "--reason", "Still empty",
                ],
            )
            self.assertEqual(run["returncode"], 1)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["status"], "warn")
            self.assertTrue(actual["data"]["duplicate"])


class TestRemoveItem(unittest.TestCase):
    def test_remove_existing_item(self):
        """--remove takes an item off the 86 list."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            shutil.copy(
                FIXTURES / "warn_case" / "current.md",
                Path(tmpdir) / "current.md",
            )
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=["--remove", "Golden Horizon IPA"],
            )
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["data"]["item"], "Golden Horizon IPA")
            self.assertTrue(actual["data"]["found"])
            self.assertEqual(actual["findings"][0]["code"], "ITEM_BACK")

            # Verify item removed from file
            content = (Path(tmpdir) / "current.md").read_text()
            self.assertNotIn("Golden Horizon IPA", content)
            self.assertIn("Midnight Velvet Bourbon", content)

    def test_remove_nonexistent_item(self):
        """--remove of item not on list returns ok with found=False."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            shutil.copy(
                FIXTURES / "warn_case" / "current.md",
                Path(tmpdir) / "current.md",
            )
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=["--remove", "Phantom Ale"],
            )
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertFalse(actual["data"]["found"])

    def test_remove_from_missing_file(self):
        """--remove when no 86 file exists returns ok."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            run = _run_skill(
                data_dir=tmpdir,
                extra_args=["--remove", "Phantom Ale"],
            )
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertFalse(actual["data"]["found"])


class TestDefaultBehavior(unittest.TestCase):
    def test_no_flags_defaults_to_list(self):
        """No action flags should behave like --list."""
        fixture_dir = str(FIXTURES / "warn_case")
        run = _run_skill(data_dir=fixture_dir)
        self.assertEqual(run["returncode"], 1)
        actual = json.loads(run["stdout"])
        self.assertEqual(actual["status"], "warn")
        self.assertEqual(len(actual["findings"]), 2)

    def test_missing_file_returns_all_clear(self):
        """--list on nonexistent file returns all clear."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            run = _run_skill(data_dir=tmpdir, extra_args=["--list"])
            self.assertEqual(run["returncode"], 0)
            actual = json.loads(run["stdout"])
            self.assertEqual(actual["status"], "ok")
            self.assertIn("All clear", actual["summary"])


class TestCodeQuality(unittest.TestCase):
    """Grep-based checks: no print(), no open(), no f-string in log events."""

    def test_no_print_calls(self):
        """No print() in skill code."""
        code = (Path(__file__).parent / "main.py").read_text()
        for i, line in enumerate(code.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "print(" in line:
                self.fail("print() found at line {line}".format(line=i))

    def test_no_direct_open(self):
        """No direct open() calls in skill code."""
        code = (Path(__file__).parent / "main.py").read_text()
        for i, line in enumerate(code.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if "open(" in line:
                self.fail("open() found at line {line}".format(line=i))

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
                manifest[field],
                skill_md,
                "{field} mismatch".format(field=field),
            )


if __name__ == "__main__":
    unittest.main()
