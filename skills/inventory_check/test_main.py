"""Tests for inventory-check skill. stdlib unittest, golden-output pattern."""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _run_skill(fixture_dir: str | None = None, fmt: str = "json") -> dict:
    """Run inventory-check as a subprocess, return parsed result."""
    cmd = [sys.executable, "-m", "skills.inventory_check", "--format", fmt]
    if fixture_dir:
        cmd.extend(["--inventory-dir", fixture_dir])
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
        fixture_dir = str(FIXTURES / "happy_path")
        run = _run_skill(fixture_dir)
        self.assertEqual(run["returncode"], 0)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "happy_path" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))


class TestLowStock(unittest.TestCase):
    def test_low_stock_golden(self):
        """Run against low_stock fixtures, assert status warn and 2 findings."""
        fixture_dir = str(FIXTURES / "low_stock")
        run = _run_skill(fixture_dir)
        self.assertEqual(run["returncode"], 1)

        actual = json.loads(run["stdout"])
        with (FIXTURES / "low_stock" / "expected.json").open() as f:
            expected = json.load(f)

        self.assertEqual(_strip_duration(actual), _strip_duration(expected))
        self.assertEqual(actual["status"], "warn")
        self.assertEqual(len(actual["findings"]), 2)


class TestMalformed(unittest.TestCase):
    def test_malformed_skipped(self):
        """Malformed fixtures should not crash the skill."""
        fixture_dir = str(FIXTURES / "malformed")
        run = _run_skill(fixture_dir)
        # Should complete without error (exit 0, no findings from bad table)
        self.assertIn(run["returncode"], (0, 1))
        actual = json.loads(run["stdout"])
        self.assertIn(actual["status"], ("ok", "warn"))


class TestEdgeCases(unittest.TestCase):
    def test_empty_qty_rows_skipped(self):
        """Rows with empty qty should NOT be treated as qty=0."""
        from skills._lib.md_table import parse_tables

        text = (
            "| Item | Qty | Reorder at |\n"
            "|------|-----|------------|\n"
            "| Widget |  | 5 |\n"
        )
        tables = parse_tables(text)
        self.assertEqual(len(tables), 1)
        row = tables[0][0]
        # qty is empty string, _parse_int should return None
        from skills.inventory_check.main import _parse_int
        self.assertIsNone(_parse_int(row.get("qty")))

    def test_path_traversal_rejected(self):
        """read_allowed_path must raise PermissionError for traversal."""
        from skills._lib.io import read_allowed_path

        docs_root = REPO_ROOT / "docs" / "inventory"
        bad_path = docs_root / ".." / ".." / ".." / "etc" / "passwd"
        with self.assertRaises(PermissionError):
            read_allowed_path(bad_path, allowlist_root=docs_root)


class TestParserCaps(unittest.TestCase):
    def test_md_table_size_cap(self):
        """Parser should refuse input larger than 262144 bytes."""
        from skills._lib.md_table import parse_tables

        big_text = "| A | B |\n|---|---|\n" + ("| x | y |\n" * 30000)
        self.assertGreater(len(big_text.encode("utf-8")), 262144)
        tables = parse_tables(big_text)
        self.assertEqual(tables, [])

    def test_md_table_row_cap(self):
        """Parser should stop at 500 rows per table."""
        from skills._lib.md_table import parse_tables

        # Build a table with 600 rows but small enough in bytes
        header = "| A | B |\n|---|---|\n"
        rows = "| x | y |\n" * 600
        text = header + rows
        # Ensure it's under the byte cap
        self.assertLess(len(text.encode("utf-8")), 262144)
        tables = parse_tables(text)
        self.assertEqual(len(tables), 1)
        self.assertEqual(len(tables[0]), 500)


class TestCodeQuality(unittest.TestCase):
    """Grep-based checks: no print(), no open(), no f-string in log events."""

    _SKILL_CODE_FILES: list[Path] = []

    @classmethod
    def setUpClass(cls):
        lib_dir = REPO_ROOT / "skills" / "_lib"
        skill_dir = REPO_ROOT / "skills" / "inventory_check"
        cls._SKILL_CODE_FILES = []
        for d in (lib_dir, skill_dir):
            for py in d.glob("*.py"):
                if py.name.startswith("test_"):
                    continue
                cls._SKILL_CODE_FILES.append(py)

    def test_no_print_calls(self):
        """No print() calls in skill or _lib code (excluding tests)."""
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
        """No direct open() calls in skill code (excluding _lib and tests)."""
        violations = []
        skill_dir = REPO_ROOT / "skills" / "inventory_check"
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
            # Find log.event( calls with f-string as first arg
            for i, line in enumerate(content.splitlines(), 1):
                if "log.event(" in line and 'f"' in line or "f'" in line:
                    if "log.event(" in line:
                        violations.append("{file}:{line}".format(file=py.name, line=i))
        self.assertEqual(
            violations, [], "f-string in log.event: " + ", ".join(violations)
        )


if __name__ == "__main__":
    unittest.main()
