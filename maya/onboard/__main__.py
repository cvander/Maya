"""CLI entry point: python -m maya.onboard"""

import argparse
import sys
from pathlib import Path

from maya.onboard.main import run_interactive, run_non_interactive


def main():
    parser = argparse.ArgumentParser(
        description="Maya onboarding wizard - set up your bar for Maya from your answers."
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without prompts, using a pre-filled answers JSON file.",
    )
    parser.add_argument(
        "--answers",
        default=None,
        help="Path to JSON file with answers (required for --non-interactive).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Defaults to the Maya project root.",
    )

    args = parser.parse_args()

    # Default output dir is the Maya project root
    if args.output_dir is None:
        output_dir = Path(__file__).resolve().parents[2]
    else:
        output_dir = Path(args.output_dir)

    if args.non_interactive:
        if not args.answers:
            parser.error("--answers is required when using --non-interactive")

        try:
            files = run_non_interactive(args.answers, output_dir)
            print("Generated {} files in {}\n".format(len(files), output_dir))
            for f in files:
                print("  {}".format(f))
            print("")
            return 0
        except FileNotFoundError:
            print("Error: answers file not found: {}".format(args.answers), file=sys.stderr)
            return 2
        except ValueError as e:
            print("Error: {}".format(e), file=sys.stderr)
            return 2
    else:
        try:
            files = run_interactive(output_dir)
            print("\nGenerated {} files in {}\n".format(len(files), output_dir))
            for f in files:
                print("  {}".format(f))
            print("\nYour bar is set up. Welcome to Maya.")
            return 0
        except ValueError as e:
            print("Error: {}".format(e), file=sys.stderr)
            return 2


if __name__ == "__main__":
    sys.exit(main())
