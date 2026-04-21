"""Eval: validate exit code / status mapping in expected.json files per CONTRACT.md."""

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"

# Directories to exclude (templates, shared libs)
_EXCLUDE = {"_skeleton", "_lib"}

# Skills discovered dynamically via manifest.toml
SKILL_DIRS = sorted(
    p.parent for p in SKILLS_DIR.glob("*/manifest.toml")
    if p.parent.name not in _EXCLUDE
)

# CONTRACT.md exit code mapping
STATUS_TO_EXIT_CODE = {
    "ok": 0,
    "warn": 1,
    # "fail" maps to 2 (config) or 3 (data) depending on context
}

VALID_STATUSES = {"ok", "warn", "fail"}


def _collect_expected_jsons(skill_dir: Path) -> list[tuple[str, dict]]:
    """Collect all expected.json files from a skill's fixtures."""
    fixtures = skill_dir / "fixtures"
    if not fixtures.is_dir():
        return []
    results = []
    for scenario_dir in sorted(fixtures.iterdir()):
        if not scenario_dir.is_dir():
            continue
        if scenario_dir.name in ("local", "__pycache__"):
            continue
        expected = scenario_dir / "expected.json"
        if expected.is_file():
            try:
                data = json.loads(expected.read_text(encoding="utf-8"))
                results.append((scenario_dir.name, data))
            except (json.JSONDecodeError, OSError):
                pass
    return results


class TestExitCodeMapping(unittest.TestCase):
    """Validate status field and exit code consistency across all expected.json."""

    def test_status_field_valid(self):
        """Every expected.json has a valid status: ok, warn, or fail."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                status = data.get("status")
                if status not in VALID_STATUSES:
                    failures.append(
                        "{}/{}: status '{}' not in {}".format(
                            skill_dir.name, scenario_name, status, VALID_STATUSES
                        )
                    )
        self.assertEqual(
            failures, [],
            "Invalid status values:\n{}".format("\n".join(failures))
        )

    def test_happy_path_status_not_fail(self):
        """happy_path fixtures should not have status 'fail'.

        Some skills produce warnings even in their standard happy_path scenario
        (e.g. cost_analysis detecting high pour costs, schedule_draft detecting
        overtime risks). This is by design - 'happy_path' means the skill runs
        correctly, not that there are zero findings.
        """
        failures = []
        for skill_dir in SKILL_DIRS:
            expected_file = skill_dir / "fixtures" / "happy_path" / "expected.json"
            if not expected_file.is_file():
                continue
            try:
                data = json.loads(expected_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                failures.append("{}: cannot parse happy_path/expected.json".format(skill_dir.name))
                continue
            if data.get("status") == "fail":
                failures.append(
                    "{}: happy_path status is 'fail'".format(skill_dir.name)
                )
        self.assertEqual(
            failures, [],
            "Happy path should not fail:\n{}".format("\n".join(failures))
        )

    def test_happy_path_no_fail_findings(self):
        """happy_path fixtures should not have fail-severity findings.

        Note: some happy_path fixtures may include informational or warn
        findings (e.g. overtime risks in an otherwise valid schedule).
        We check only for 'fail' severity in happy_path.
        """
        failures = []
        for skill_dir in SKILL_DIRS:
            expected_file = skill_dir / "fixtures" / "happy_path" / "expected.json"
            if not expected_file.is_file():
                continue
            try:
                data = json.loads(expected_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            for i, finding in enumerate(data.get("findings", [])):
                sev = finding.get("severity")
                if sev == "fail":
                    failures.append(
                        "{}: happy_path finding[{}] has severity 'fail'".format(
                            skill_dir.name, i
                        )
                    )
        self.assertEqual(
            failures, [],
            "Happy path should not have fail findings:\n{}".format("\n".join(failures))
        )

    def test_warn_case_status_warn(self):
        """Warn-type fixtures (warn_case, low_stock) should have status 'warn'."""
        warn_dirs = {"warn_case", "low_stock"}
        failures = []
        for skill_dir in SKILL_DIRS:
            fixtures = skill_dir / "fixtures"
            if not fixtures.is_dir():
                continue
            for scenario_dir in sorted(fixtures.iterdir()):
                if not scenario_dir.is_dir():
                    continue
                if scenario_dir.name not in warn_dirs:
                    continue
                expected = scenario_dir / "expected.json"
                if not expected.is_file():
                    continue
                try:
                    data = json.loads(expected.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    continue
                if data.get("status") != "warn":
                    failures.append(
                        "{}/{}: status is '{}', expected 'warn'".format(
                            skill_dir.name, scenario_dir.name, data.get("status")
                        )
                    )
        self.assertEqual(
            failures, [],
            "Warn case status issues:\n{}".format("\n".join(failures))
        )

    def test_result_has_core_fields(self):
        """Every expected.json has at minimum skill, status, and data fields."""
        core_fields = {"skill", "status", "data"}
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                missing = core_fields - set(data.keys())
                if missing:
                    failures.append(
                        "{}/{}: missing core fields {}".format(
                            skill_dir.name, scenario_name, missing
                        )
                    )
        self.assertEqual(
            failures, [],
            "Missing core Result fields:\n{}".format("\n".join(failures))
        )

    def test_result_completeness_coverage(self):
        """At least 90% of expected.json files have all CONTRACT.md Result fields.

        Some fixture files may be partial (e.g. specifying only expected codes).
        This tracks overall coverage rather than requiring 100%.
        """
        all_fields = {"skill", "status", "summary", "data", "findings", "metrics"}
        total = 0
        complete = 0
        incomplete = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                total += 1
                missing = all_fields - set(data.keys())
                if missing:
                    incomplete.append(
                        "{}/{}: missing {}".format(skill_dir.name, scenario_name, missing)
                    )
                else:
                    complete += 1
        if total == 0:
            return
        coverage = complete / total
        self.assertGreaterEqual(
            coverage, 0.90,
            "Only {:.0%} of expected.json files are complete. Incomplete:\n{}".format(
                coverage, "\n".join(incomplete)
            )
        )

    def test_skill_name_matches_manifest(self):
        """The 'skill' field in expected.json matches manifest.toml name."""
        failures = []
        for skill_dir in SKILL_DIRS:
            # Read manifest name
            import tomllib
            manifest_path = skill_dir / "manifest.toml"
            try:
                with manifest_path.open("rb") as f:
                    manifest = tomllib.load(f)
                manifest_name = manifest.get("skill", {}).get("name", "")
            except (FileNotFoundError, tomllib.TOMLDecodeError):
                continue

            for scenario_name, data in _collect_expected_jsons(skill_dir):
                result_name = data.get("skill", "")
                if result_name != manifest_name:
                    failures.append(
                        "{}/{}: skill='{}' but manifest name='{}'".format(
                            skill_dir.name, scenario_name, result_name, manifest_name
                        )
                    )
        self.assertEqual(
            failures, [],
            "Skill name mismatches:\n{}".format("\n".join(failures))
        )

    def test_findings_is_list_when_present(self):
        """When findings field exists, it is a list."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                if "findings" not in data:
                    continue  # Missing field tracked by completeness test
                findings = data["findings"]
                if not isinstance(findings, list):
                    failures.append(
                        "{}/{}: findings is {} not list".format(
                            skill_dir.name, scenario_name, type(findings).__name__
                        )
                    )
        self.assertEqual(
            failures, [],
            "Non-list findings:\n{}".format("\n".join(failures))
        )

    def test_metrics_is_dict_when_present(self):
        """When metrics field exists, it is a dict.

        Note: duration_ms is injected at runtime by the skill runner and is
        intentionally excluded from golden expected.json files (since it varies).
        The per-skill tests strip duration_ms before comparing.
        """
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                if "metrics" not in data:
                    continue
                metrics = data["metrics"]
                if not isinstance(metrics, dict):
                    failures.append(
                        "{}/{}: metrics is {} not dict".format(
                            skill_dir.name, scenario_name, type(metrics).__name__
                        )
                    )
        self.assertEqual(
            failures, [],
            "Metrics type issues:\n{}".format("\n".join(failures))
        )


if __name__ == "__main__":
    unittest.main()
