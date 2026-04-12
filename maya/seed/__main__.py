"""CLI entry point: python -m maya.seed"""

import argparse
import sys

from maya.seed.main import generate, dry_run, list_types


def main():
    parser = argparse.ArgumentParser(
        description="Maya seed generator - create fictional bar data for different bar types."
    )
    parser.add_argument(
        "--type",
        dest="bar_type",
        help="Bar type to generate (e.g. dive-bar, cocktail-lounge, sports-bar, wine-bar).",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory. Defaults to the Maya project root.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing files.",
    )
    parser.add_argument(
        "--list-types",
        action="store_true",
        help="Show available bar types and exit.",
    )

    args = parser.parse_args()

    if args.list_types:
        print("Available bar types:\n")
        for name, desc in list_types():
            print("  {:<20} {}".format(name, desc))
        print("")
        return 0

    if not args.bar_type:
        parser.error("--type is required (or use --list-types to see options)")

    # Default output dir is the Maya project root
    if args.output_dir is None:
        from pathlib import Path
        output_dir = Path(__file__).resolve().parents[2]
    else:
        from pathlib import Path
        output_dir = Path(args.output_dir)

    if args.dry_run:
        print("Dry run for '{}' -> {}\n".format(args.bar_type, output_dir))
        print("Would generate:\n")
        for path in dry_run(args.bar_type, output_dir):
            print("  {}".format(path))
        print("")
        return 0

    try:
        files = generate(args.bar_type, output_dir)
        print("Generated {} files for '{}' in {}\n".format(
            len(files), args.bar_type, output_dir
        ))
        for f in files:
            print("  {}".format(f))
        print("")
        return 0
    except ValueError as e:
        print("Error: {}".format(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
