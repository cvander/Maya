"""Integration test: inventory-check qty=0 items get auto-86'd."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "skills" / "inventory_check" / "fixtures"


def _run_skill(module: str, extra_args: list[str] | None = None) -> dict:
    """Run a skill as a subprocess and return parsed result."""
    cmd = [sys.executable, "-m", module, "--format", "json"]
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


class TestEightySixFromInventory(unittest.TestCase):
    """inventory-check qty=0 items should be 86-able."""

    def test_zero_qty_items_can_be_86d(self):
        """Items with qty=0 from inventory-check should be addable to 86 list."""
        # Step 1: Run inventory-check against low_stock fixtures
        fixture_dir = str(FIXTURES / "low_stock")
        inv_run = _run_skill(
            "skills.inventory_check",
            ["--inventory-dir", fixture_dir],
        )
        self.assertIn(inv_run["returncode"], (0, 1))
        inv_result = json.loads(inv_run["stdout"])

        # Step 2: Find items with qty=0
        zero_items = [
            item for item in inv_result["data"]["low_stock"]
            if item["qty"] == 0
        ]
        self.assertGreater(
            len(zero_items), 0,
            "Expected at least one item with qty=0 in low_stock fixtures",
        )

        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            # Step 3: Add each zero-qty item to the 86 list
            for item in zero_items:
                add_run = _run_skill(
                    "skills.eighty_six",
                    [
                        "--add", item["item"],
                        "--reason", "Out of stock (qty=0)",
                        "--reported-by", "Integration Test",
                        "--data-dir", tmpdir,
                        "--inventory-dir", fixture_dir,
                    ],
                )
                self.assertIn(
                    add_run["returncode"], (0, 1),
                    "eighty-six --add failed for {item} with exit code {code}:\n{err}".format(
                        item=item["item"],
                        code=add_run["returncode"],
                        err=add_run["stderr"],
                    ),
                )
                add_result = json.loads(add_run["stdout"])
                self.assertEqual(
                    add_result["data"]["action"], "add",
                    "Expected action=add for {item}".format(item=item["item"]),
                )

            # Step 4: List the 86 list and verify items appear
            list_run = _run_skill(
                "skills.eighty_six",
                ["--list", "--data-dir", tmpdir],
            )
            self.assertIn(list_run["returncode"], (0, 1))
            list_result = json.loads(list_run["stdout"])

            listed_items = {
                i["item"] for i in list_result["data"]["items"]
            }
            expected_items = {item["item"] for item in zero_items}

            self.assertTrue(
                expected_items.issubset(listed_items),
                "Expected 86'd items {expected} to be in list {actual}".format(
                    expected=sorted(expected_items),
                    actual=sorted(listed_items),
                ),
            )

    def test_duplicate_86_is_handled(self):
        """Adding the same item twice to 86 list should not crash."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            fixture_dir = str(FIXTURES / "low_stock")
            item_name = "Test Duplicate Item"

            # Add once
            _run_skill(
                "skills.eighty_six",
                [
                    "--add", item_name,
                    "--reason", "First add",
                    "--data-dir", tmpdir,
                    "--inventory-dir", fixture_dir,
                ],
            )

            # Add again - should not crash
            dup_run = _run_skill(
                "skills.eighty_six",
                [
                    "--add", item_name,
                    "--reason", "Second add",
                    "--data-dir", tmpdir,
                    "--inventory-dir", fixture_dir,
                ],
            )
            self.assertIn(dup_run["returncode"], (0, 1))
            dup_result = json.loads(dup_run["stdout"])
            self.assertTrue(
                dup_result["data"].get("duplicate", False),
                "Second add should report duplicate=True",
            )


if __name__ == "__main__":
    unittest.main()
