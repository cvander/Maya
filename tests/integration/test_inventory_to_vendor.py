"""Integration test: inventory-check output feeds into vendor-order-review."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "skills" / "inventory_check" / "fixtures"
VENDOR_FIXTURES = REPO_ROOT / "skills" / "vendor_order_review" / "fixtures"


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


class TestInventoryToVendorChain(unittest.TestCase):
    """Run inventory-check -> vendor-order-review chain."""

    def test_low_stock_generates_order_recommendations(self):
        """inventory-check low_stock output should produce ORDER_NEEDED findings
        when fed to vendor-order-review."""
        # Step 1: Run inventory-check against low_stock fixtures
        fixture_dir = str(FIXTURES / "low_stock")
        inv_run = _run_skill(
            "skills.inventory_check",
            ["--inventory-dir", fixture_dir],
        )
        self.assertIn(
            inv_run["returncode"], (0, 1),
            "inventory-check failed with exit code {code}:\n{err}".format(
                code=inv_run["returncode"], err=inv_run["stderr"],
            ),
        )
        inv_result = json.loads(inv_run["stdout"])
        self.assertEqual(inv_result["status"], "warn")
        self.assertGreater(len(inv_result["data"]["low_stock"]), 0)

        # Step 2: Save inventory-check output to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            json.dump(inv_result, tmp)
            tmp_path = tmp.name

        try:
            # Step 3: Run vendor-order-review with the temp file as input
            # Use vendor fixtures dir for vendor map
            vendor_fixture_dir = str(VENDOR_FIXTURES / "warn_case")
            vor_run = _run_skill(
                "skills.vendor_order_review",
                [
                    "--input-file", tmp_path,
                    "--inventory-dir", vendor_fixture_dir,
                ],
            )
            self.assertIn(
                vor_run["returncode"], (0, 1),
                "vendor-order-review failed with exit code {code}:\n{err}".format(
                    code=vor_run["returncode"], err=vor_run["stderr"],
                ),
            )
            vor_result = json.loads(vor_run["stdout"])

            # Step 4: Verify ORDER_NEEDED findings exist
            order_findings = [
                f for f in vor_result["findings"]
                if f["code"] == "ORDER_NEEDED"
            ]
            self.assertGreater(
                len(order_findings), 0,
                "Expected ORDER_NEEDED findings but got none.",
            )

            # Step 5: Verify order quantities are positive
            for order_vendor_items in vor_result["data"]["orders_by_vendor"].values():
                for order in order_vendor_items:
                    self.assertGreater(
                        order["order_qty"], 0,
                        "Order quantity should be positive for {item}".format(
                            item=order["item"],
                        ),
                    )
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_no_low_stock_produces_no_orders(self):
        """When inventory has no low-stock items, vendor-order-review should
        produce zero orders."""
        # Run inventory-check against happy_path fixtures (nothing low)
        fixture_dir = str(FIXTURES / "happy_path")
        inv_run = _run_skill(
            "skills.inventory_check",
            ["--inventory-dir", fixture_dir],
        )
        self.assertEqual(inv_run["returncode"], 0)
        inv_result = json.loads(inv_run["stdout"])
        self.assertEqual(inv_result["status"], "ok")
        self.assertEqual(len(inv_result["data"]["low_stock"]), 0)

        # Feed to vendor-order-review
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            json.dump(inv_result, tmp)
            tmp_path = tmp.name

        try:
            vor_run = _run_skill(
                "skills.vendor_order_review",
                [
                    "--input-file", tmp_path,
                    "--inventory-dir", str(VENDOR_FIXTURES / "happy_path"),
                ],
            )
            self.assertEqual(vor_run["returncode"], 0)
            vor_result = json.loads(vor_run["stdout"])
            self.assertEqual(vor_result["status"], "ok")
            self.assertEqual(len(vor_result["findings"]), 0)
        finally:
            Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
