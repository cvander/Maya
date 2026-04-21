"""Contract compliance tests: verify every skill follows CONTRACT.md structure."""

import ast
import re
import tomllib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"

# Required fields in manifest.toml [skill] table
MANIFEST_REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "safety",
    "pii_scope",
    "failure_mode",
    "reads",
    "writes",
    "network",
    "hard_stops_touched",
    "env_required",
]

# Directories to exclude from skill discovery
_EXCLUDE_DIRS = {"_lib", "_skeleton", "__pycache__"}


def _discover_skills() -> list[Path]:
    """Discover skill directories by finding all manifest.toml files."""
    skills = []
    for manifest in sorted(SKILLS_DIR.glob("*/manifest.toml")):
        skill_dir = manifest.parent
        if skill_dir.name in _EXCLUDE_DIRS:
            continue
        skills.append(skill_dir)
    return skills


class TestContractCompliance(unittest.TestCase):
    """Verify every skill directory follows CONTRACT.md structure."""

    _skills: list[Path] = []

    @classmethod
    def setUpClass(cls):
        cls._skills = _discover_skills()
        if not cls._skills:
            raise unittest.SkipTest("No skills found under skills/")

    def test_skills_discovered(self):
        """At least one skill should be discovered."""
        self.assertGreater(len(self._skills), 0)

    def test_has_init_py(self):
        """Every skill must have __init__.py."""
        missing = [
            s.name for s in self._skills
            if not (s / "__init__.py").is_file()
        ]
        self.assertEqual(
            missing, [],
            "__init__.py missing in: {dirs}".format(dirs=", ".join(missing)),
        )

    def test_has_main_entry(self):
        """Every skill must have __main__.py."""
        missing = [
            s.name for s in self._skills
            if not (s / "__main__.py").is_file()
        ]
        self.assertEqual(
            missing, [],
            "__main__.py missing in: {dirs}".format(dirs=", ".join(missing)),
        )

    def test_has_main_py_with_run(self):
        """Every skill must have main.py with a run() function."""
        missing_file = []
        missing_run = []
        for s in self._skills:
            main_py = s / "main.py"
            if not main_py.is_file():
                missing_file.append(s.name)
                continue
            source = main_py.read_text(encoding="utf-8")
            tree = ast.parse(source)
            func_names = [
                node.name for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            ]
            if "run" not in func_names:
                missing_run.append(s.name)

        self.assertEqual(
            missing_file, [],
            "main.py missing in: {dirs}".format(dirs=", ".join(missing_file)),
        )
        self.assertEqual(
            missing_run, [],
            "run() function missing in main.py of: {dirs}".format(
                dirs=", ".join(missing_run)
            ),
        )

    def test_has_manifest_toml_with_required_fields(self):
        """Every skill must have manifest.toml with all required fields."""
        errors = []
        for s in self._skills:
            manifest_path = s / "manifest.toml"
            # manifest existence is guaranteed by discovery
            with manifest_path.open("rb") as f:
                data = tomllib.load(f)
            skill_section = data.get("skill", {})
            missing_fields = [
                field for field in MANIFEST_REQUIRED_FIELDS
                if field not in skill_section
            ]
            if missing_fields:
                errors.append(
                    "{name}: missing {fields}".format(
                        name=s.name,
                        fields=", ".join(missing_fields),
                    )
                )
        self.assertEqual(
            errors, [],
            "Manifest field violations:\n  " + "\n  ".join(errors) if errors else "",
        )

    def test_has_skill_md(self):
        """Every skill must have SKILL.md."""
        missing = [
            s.name for s in self._skills
            if not (s / "SKILL.md").is_file()
        ]
        self.assertEqual(
            missing, [],
            "SKILL.md missing in: {dirs}".format(dirs=", ".join(missing)),
        )

    def test_has_test_main_py(self):
        """Every skill must have test_main.py."""
        missing = [
            s.name for s in self._skills
            if not (s / "test_main.py").is_file()
        ]
        self.assertEqual(
            missing, [],
            "test_main.py missing in: {dirs}".format(dirs=", ".join(missing)),
        )

    def test_has_fixtures_dir_with_fixtures_md(self):
        """Every skill must have a fixtures/ directory with FIXTURES.md."""
        missing_dir = []
        missing_md = []
        for s in self._skills:
            fixtures_dir = s / "fixtures"
            if not fixtures_dir.is_dir():
                missing_dir.append(s.name)
                continue
            if not (fixtures_dir / "FIXTURES.md").is_file():
                missing_md.append(s.name)

        self.assertEqual(
            missing_dir, [],
            "fixtures/ directory missing in: {dirs}".format(
                dirs=", ".join(missing_dir)
            ),
        )
        self.assertEqual(
            missing_md, [],
            "fixtures/FIXTURES.md missing in: {dirs}".format(
                dirs=", ".join(missing_md)
            ),
        )

    def test_main_py_no_print_calls(self):
        """main.py must not contain print() calls (excluding comments)."""
        violations = []
        for s in self._skills:
            main_py = s / "main.py"
            if not main_py.is_file():
                continue
            for i, line in enumerate(
                main_py.read_text(encoding="utf-8").splitlines(), 1
            ):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "print(" in line:
                    violations.append(
                        "{name}/main.py:{line}".format(name=s.name, line=i)
                    )
        self.assertEqual(
            violations, [],
            "print() calls found in: " + ", ".join(violations),
        )

    def test_main_py_no_direct_open(self):
        """main.py must not contain direct open() calls (excluding comments)."""
        violations = []
        for s in self._skills:
            main_py = s / "main.py"
            if not main_py.is_file():
                continue
            for i, line in enumerate(
                main_py.read_text(encoding="utf-8").splitlines(), 1
            ):
                stripped = line.strip()
                if stripped.startswith("#"):
                    continue
                if "open(" in line:
                    violations.append(
                        "{name}/main.py:{line}".format(name=s.name, line=i)
                    )
        self.assertEqual(
            violations, [],
            "open() calls found in: " + ", ".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
