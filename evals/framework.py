"""Maya eval framework. Runs offline or CI-only evals."""

import argparse
import sys
import unittest
from pathlib import Path


EVALS_DIR = Path(__file__).resolve().parent


def run_offline() -> bool:
    """Run deterministic evals (no API key needed)."""
    loader = unittest.TestLoader()
    suite = loader.discover(str(EVALS_DIR / "offline"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_ci() -> bool:
    """Run CI-only evals (require Hermes + API key)."""
    # Placeholder - these will be implemented when Hermes integration is ready
    print("CI-only evals require Hermes + OPENROUTER_API_KEY")
    print("Skipping CI-only evals (not yet implemented)")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Maya eval framework")
    parser.add_argument("--offline", action="store_true", help="Run offline evals only")
    parser.add_argument("--ci", action="store_true", help="Run CI-only evals")
    parser.add_argument("--all", action="store_true", help="Run all evals")
    args = parser.parse_args()

    if not (args.offline or args.ci or args.all):
        args.offline = True  # default

    success = True
    if args.offline or args.all:
        success = run_offline() and success
    if args.ci or args.all:
        success = run_ci() and success

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
