"""Eval: verify every skill has adequate fixture coverage."""

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


class TestFixtureCoverage(unittest.TestCase):
    """Verify fixture directories and minimum scenario count for every skill."""

    def test_fixtures_dir_exists(self):
        """Every skill has a fixtures/ directory."""
        missing = []
        for skill_dir in SKILL_DIRS:
            fixtures = skill_dir / "fixtures"
            if not fixtures.is_dir():
                missing.append(skill_dir.name)
        self.assertEqual(missing, [], "Skills missing fixtures/: {}".format(missing))

    def test_happy_path_exists(self):
        """Every skill has a fixtures/happy_path/ directory."""
        missing = []
        for skill_dir in SKILL_DIRS:
            happy = skill_dir / "fixtures" / "happy_path"
            if not happy.is_dir():
                missing.append(skill_dir.name)
        self.assertEqual(missing, [], "Skills missing fixtures/happy_path/: {}".format(missing))

    def test_happy_path_has_expected_json(self):
        """Every happy_path/ directory has an expected.json file."""
        missing = []
        for skill_dir in SKILL_DIRS:
            expected = skill_dir / "fixtures" / "happy_path" / "expected.json"
            if not expected.is_file():
                missing.append(skill_dir.name)
        self.assertEqual(missing, [], "Skills missing happy_path/expected.json: {}".format(missing))

    def test_warn_case_exists(self):
        """Every skill has a warn-type fixture directory.

        Accepts either warn_case/ or a skill-specific equivalent like low_stock/.
        Skills with only happy_path are noted via subTest but do not fail.
        """
        missing = []
        for skill_dir in SKILL_DIRS:
            fixtures = skill_dir / "fixtures"
            if not fixtures.is_dir():
                missing.append(skill_dir.name)
                continue
            # Look for any fixture dir that is not happy_path, local, or __pycache__
            subdirs = [
                d.name for d in fixtures.iterdir()
                if d.is_dir() and d.name not in ("happy_path", "local", "__pycache__")
            ]
            if not subdirs:
                # Report via subTest - not a hard failure since some skills
                # (e.g. report aggregators) may only have happy_path
                with self.subTest(skill=skill_dir.name):
                    missing.append(skill_dir.name)
        # At least 80% of skills should have warn/edge scenarios
        coverage = 1 - (len(missing) / len(SKILL_DIRS)) if SKILL_DIRS else 0
        self.assertGreaterEqual(
            coverage, 0.80,
            "Only {:.0%} of skills have warn/edge fixtures. Missing: {}".format(
                coverage, missing
            )
        )

    def test_minimum_two_scenarios(self):
        """Most skills have at least 2 fixture scenarios (directories)."""
        insufficient = []
        for skill_dir in SKILL_DIRS:
            fixtures = skill_dir / "fixtures"
            if not fixtures.is_dir():
                insufficient.append(skill_dir.name)
                continue
            scenario_dirs = [
                d for d in fixtures.iterdir()
                if d.is_dir() and d.name not in ("local", "__pycache__")
            ]
            if len(scenario_dirs) < 2:
                insufficient.append(skill_dir.name)
        # At least 80% of skills should have 2+ scenarios
        coverage = 1 - (len(insufficient) / len(SKILL_DIRS)) if SKILL_DIRS else 0
        self.assertGreaterEqual(
            coverage, 0.80,
            "Only {:.0%} of skills have 2+ fixture scenarios. Insufficient: {}".format(
                coverage, insufficient
            )
        )


if __name__ == "__main__":
    unittest.main()
