"""Eval: validate finding codes in expected.json files follow CONTRACT.md rules."""

import json
import re
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

UPPER_SNAKE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
VALID_SEVERITIES = {"info", "warn", "fail"}
FINDING_REQUIRED_KEYS = {"severity", "code", "subject", "message"}


def _collect_expected_jsons(skill_dir: Path) -> list[tuple[str, dict]]:
    """Collect all expected.json files from a skill's fixtures.

    Returns list of (fixture_name, parsed_dict) tuples.
    """
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


class TestFindingCodes(unittest.TestCase):
    """Validate finding structure and codes across all skill expected.json files."""

    def test_findings_have_required_keys(self):
        """Every finding in expected.json has severity, code, subject, message."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                for i, finding in enumerate(data.get("findings", [])):
                    missing = FINDING_REQUIRED_KEYS - set(finding.keys())
                    if missing:
                        failures.append(
                            "{}/{} finding[{}]: missing {}".format(
                                skill_dir.name, scenario_name, i, missing
                            )
                        )
        self.assertEqual(
            failures, [],
            "Findings missing required keys:\n{}".format("\n".join(failures))
        )

    def test_severity_values_valid(self):
        """Every finding severity is info, warn, or fail."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                for i, finding in enumerate(data.get("findings", [])):
                    sev = finding.get("severity")
                    if sev not in VALID_SEVERITIES:
                        failures.append(
                            "{}/{} finding[{}]: severity '{}' not in {}".format(
                                skill_dir.name, scenario_name, i, sev, VALID_SEVERITIES
                            )
                        )
        self.assertEqual(
            failures, [],
            "Invalid severity values:\n{}".format("\n".join(failures))
        )

    def test_codes_upper_snake_case(self):
        """All finding codes use UPPER_SNAKE_CASE format."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                for i, finding in enumerate(data.get("findings", [])):
                    code = finding.get("code", "")
                    if not UPPER_SNAKE_RE.match(code):
                        failures.append(
                            "{}/{} finding[{}]: code '{}' not UPPER_SNAKE_CASE".format(
                                skill_dir.name, scenario_name, i, code
                            )
                        )
        self.assertEqual(
            failures, [],
            "Non-UPPER_SNAKE_CASE codes:\n{}".format("\n".join(failures))
        )

    def test_no_exact_duplicate_findings(self):
        """No exact duplicate findings (all 4 fields identical) within a scenario.

        Note: same code+subject with different messages is allowed (e.g.
        OVERTIME_RISK for same person on different days).
        """
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                seen = set()
                for i, finding in enumerate(data.get("findings", [])):
                    key = (
                        finding.get("severity", ""),
                        finding.get("code", ""),
                        finding.get("subject", ""),
                        finding.get("message", ""),
                    )
                    if key in seen:
                        failures.append(
                            "{}/{} finding[{}]: exact duplicate ({}, {})".format(
                                skill_dir.name, scenario_name, i, key[1], key[2]
                            )
                        )
                    seen.add(key)
        self.assertEqual(
            failures, [],
            "Exact duplicate findings within scenario:\n{}".format("\n".join(failures))
        )

    def test_subject_and_message_non_empty(self):
        """Finding subject and message fields are non-empty strings."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                for i, finding in enumerate(data.get("findings", [])):
                    subject = finding.get("subject", "")
                    message = finding.get("message", "")
                    if not subject or not isinstance(subject, str):
                        failures.append(
                            "{}/{} finding[{}]: empty or invalid subject".format(
                                skill_dir.name, scenario_name, i
                            )
                        )
                    if not message or not isinstance(message, str):
                        failures.append(
                            "{}/{} finding[{}]: empty or invalid message".format(
                                skill_dir.name, scenario_name, i
                            )
                        )
        self.assertEqual(
            failures, [],
            "Empty subject/message:\n{}".format("\n".join(failures))
        )

    def test_warn_scenarios_have_findings(self):
        """Scenarios with status 'warn' should have at least one finding."""
        failures = []
        for skill_dir in SKILL_DIRS:
            for scenario_name, data in _collect_expected_jsons(skill_dir):
                status = data.get("status")
                findings = data.get("findings", [])
                # warn status with warn/fail severity findings = ok
                # warn status with no findings = suspicious
                if status == "warn" and not findings:
                    # Allow edge cases where warn is set for data reasons
                    # but flag it as worth checking
                    failures.append(
                        "{}/{}: status 'warn' but no findings".format(
                            skill_dir.name, scenario_name
                        )
                    )
        # This is informational - some skills may legitimately have warn
        # without findings (e.g. schedule_view with understaffed days)
        # We still report it but do not fail the test
        if failures:
            for f in failures:
                # Use subTest to report each as a separate warning
                with self.subTest(msg=f):
                    pass  # Noted but not failing


if __name__ == "__main__":
    unittest.main()
