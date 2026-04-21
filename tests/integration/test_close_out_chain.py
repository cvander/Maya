"""Integration test: close-out writes a file, close-out-report reads it."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


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


class TestCloseOutChain(unittest.TestCase):
    """Run close-out -> close-out-report chain."""

    def test_close_out_to_report(self):
        """close-out should write a file that close-out-report can aggregate."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            # Step 1: Run close-out for two fictional dates
            dates_and_args = [
                {
                    "date": "2026-04-10",
                    "cash_count": "450.00",
                    "card_total": "1200.00",
                    "expected": "1650.00",
                    "tip_total": "180.00",
                    "waste_items": "Broken Pint Glass:2",
                },
                {
                    "date": "2026-04-11",
                    "cash_count": "520.00",
                    "card_total": "1350.00",
                    "expected": "1850.00",
                    "tip_total": "220.00",
                    "waste_items": "Flat Keg:1,Spoiled Lime:3",
                },
            ]

            for day in dates_and_args:
                co_run = _run_skill(
                    "skills.close_out",
                    [
                        "--date", day["date"],
                        "--cash-count", day["cash_count"],
                        "--card-total", day["card_total"],
                        "--expected", day["expected"],
                        "--tip-total", day["tip_total"],
                        "--waste-items", day["waste_items"],
                        "--data-dir", tmpdir,
                    ],
                )
                self.assertIn(
                    co_run["returncode"], (0, 1),
                    "close-out failed for {date} with exit code {code}:\n{err}".format(
                        date=day["date"],
                        code=co_run["returncode"],
                        err=co_run["stderr"],
                    ),
                )
                co_result = json.loads(co_run["stdout"])
                self.assertIn(
                    co_result["status"], ("ok", "warn"),
                    "close-out status unexpected: {status}".format(
                        status=co_result["status"],
                    ),
                )

            # Verify the files were written
            written = list(Path(tmpdir).glob("*.md"))
            self.assertEqual(
                len(written), 2,
                "Expected 2 close-out files, found {n}: {files}".format(
                    n=len(written),
                    files=[f.name for f in written],
                ),
            )

            # Step 2: Run close-out-report against the temp dir
            cr_run = _run_skill(
                "skills.close_out_report",
                ["--data-dir", tmpdir],
            )
            self.assertIn(
                cr_run["returncode"], (0, 1),
                "close-out-report failed with exit code {code}:\n{err}".format(
                    code=cr_run["returncode"], err=cr_run["stderr"],
                ),
            )
            cr_result = json.loads(cr_run["stdout"])

            # Step 3: Verify report aggregates the close-out data
            self.assertEqual(cr_result["status"], "ok")
            self.assertEqual(
                cr_result["data"]["days"], 2,
                "Report should cover 2 days",
            )

            # Verify revenue aggregation: 1650 + 1870 = 3520
            # Day 1: 450 + 1200 = 1650
            # Day 2: 520 + 1350 = 1870
            expected_revenue = 1650.00 + 1870.00
            self.assertAlmostEqual(
                cr_result["data"]["total_revenue"],
                expected_revenue,
                places=2,
                msg="Total revenue should be {expected}".format(
                    expected=expected_revenue,
                ),
            )

            # Verify date range
            self.assertEqual(
                cr_result["data"]["date_range"]["from"], "2026-04-10",
            )
            self.assertEqual(
                cr_result["data"]["date_range"]["to"], "2026-04-11",
            )

    def test_close_out_with_date_filter(self):
        """close-out-report should respect --from and --to date filters."""
        with tempfile.TemporaryDirectory(dir=str(REPO_ROOT / "data")) as tmpdir:
            # Write 3 days of close-out data
            for day_num in range(8, 11):
                date_str = "2026-04-{d:02d}".format(d=day_num)
                _run_skill(
                    "skills.close_out",
                    [
                        "--date", date_str,
                        "--cash-count", "500.00",
                        "--card-total", "1000.00",
                        "--expected", "1500.00",
                        "--data-dir", tmpdir,
                    ],
                )

            # Filter to only the last 2 days
            cr_run = _run_skill(
                "skills.close_out_report",
                [
                    "--data-dir", tmpdir,
                    "--from", "2026-04-09",
                    "--to", "2026-04-10",
                ],
            )
            cr_result = json.loads(cr_run["stdout"])
            self.assertEqual(
                cr_result["data"]["days"], 2,
                "Date filter should yield 2 days",
            )


if __name__ == "__main__":
    unittest.main()
