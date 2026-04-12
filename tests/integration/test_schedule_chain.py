"""Integration test: schedule-view output feeds into schedule-notify."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_FIXTURES = REPO_ROOT / "skills" / "schedule_view" / "fixtures"


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


class TestScheduleChain(unittest.TestCase):
    """Run schedule-view -> schedule-notify chain."""

    def test_schedule_view_to_notify(self):
        """schedule-view output should produce notifications for each staff member."""
        # Step 1: Run schedule-view against fixtures
        fixture_dir = str(SCHEDULE_FIXTURES / "happy_path")
        sv_run = _run_skill(
            "skills.schedule_view",
            ["--schedule-dir", fixture_dir],
        )
        self.assertEqual(
            sv_run["returncode"], 0,
            "schedule-view failed with exit code {code}:\n{err}".format(
                code=sv_run["returncode"], err=sv_run["stderr"],
            ),
        )
        sv_result = json.loads(sv_run["stdout"])
        self.assertEqual(sv_result["status"], "ok")
        self.assertGreater(len(sv_result["data"]["entries"]), 0)

        # Collect unique staff names from schedule-view output
        staff_names = set()
        for entry in sv_result["data"]["entries"]:
            name = entry.get("staff", "")
            if name:
                staff_names.add(name)
        self.assertGreater(len(staff_names), 0, "No staff names in schedule")

        # Step 2: Save schedule-view output to temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp:
            json.dump(sv_result, tmp)
            tmp_path = tmp.name

        try:
            # Step 3: Run schedule-notify with the temp file
            sn_run = _run_skill(
                "skills.schedule_notify",
                ["--input-file", tmp_path],
            )
            self.assertEqual(
                sn_run["returncode"], 0,
                "schedule-notify failed with exit code {code}:\n{err}".format(
                    code=sn_run["returncode"], err=sn_run["stderr"],
                ),
            )
            sn_result = json.loads(sn_run["stdout"])
            self.assertEqual(sn_result["status"], "ok")

            # Step 4: Verify notifications generated for each staff member
            notifications = sn_result["data"]["notifications"]
            notified_names = {n["staff"] for n in notifications}

            self.assertEqual(
                notified_names, staff_names,
                "Expected notifications for {expected} but got {actual}".format(
                    expected=sorted(staff_names),
                    actual=sorted(notified_names),
                ),
            )

            # Verify each notification has content
            for notif in notifications:
                self.assertGreater(
                    notif["shift_count"], 0,
                    "Notification for {staff} has 0 shifts".format(
                        staff=notif["staff"],
                    ),
                )
                self.assertGreater(
                    len(notif["message"]), 0,
                    "Notification for {staff} has empty message".format(
                        staff=notif["staff"],
                    ),
                )
        finally:
            Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
