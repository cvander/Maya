"""Discover and run all tests: cross-cutting tests + per-skill tests."""

import importlib
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Ensure repo root is on sys.path for imports
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

_EXCLUDE_DIRS = {"_lib", "_skeleton", "__pycache__"}


def _collect_skill_tests(loader: unittest.TestLoader) -> unittest.TestSuite:
    """Manually discover test_main.py in each skill directory.

    Skills don't live under a single importable package (no skills/__init__.py),
    so we import each test module explicitly.
    """
    suite = unittest.TestSuite()
    skills_dir = REPO_ROOT / "skills"
    for test_file in sorted(skills_dir.glob("*/test_main.py")):
        skill_name = test_file.parent.name
        if skill_name in _EXCLUDE_DIRS:
            continue
        module_name = "skills.{name}.test_main".format(name=skill_name)
        try:
            mod = importlib.import_module(module_name)
            suite.addTests(loader.loadTestsFromModule(mod))
        except Exception as exc:
            # Add a placeholder that reports the import error
            suite.addTest(
                unittest.FunctionTestCase(
                    lambda e=exc, m=module_name: (_ for _ in ()).throw(
                        ImportError("Failed to import {m}: {e}".format(m=m, e=e))
                    )
                )
            )
    return suite


if __name__ == "__main__":
    loader = unittest.TestLoader()

    # Discover cross-cutting and integration tests
    suite = loader.discover(
        str(REPO_ROOT / "tests"), pattern="test_*.py", top_level_dir=str(REPO_ROOT),
    )

    # Discover per-skill tests (test_main.py in each skill dir)
    suite.addTests(_collect_skill_tests(loader))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
