"""Core generation logic for the Maya seed generator."""

from pathlib import Path

from maya.seed.templates import TEMPLATES


def list_types():
    """Return list of available bar types with descriptions."""
    return [(name, cls.description) for name, cls in sorted(TEMPLATES.items())]


def generate(bar_type, output_dir):
    """Generate seed data for a bar type into output_dir.

    Args:
        bar_type: One of the registered template names (e.g. 'dive-bar').
        output_dir: Path where docs/ and data/ trees will be created.

    Returns:
        List of Path objects for all files created.

    Raises:
        ValueError: If bar_type is not recognized.
    """
    if bar_type not in TEMPLATES:
        raise ValueError(
            "Unknown bar type: '{}'. Available: {}".format(
                bar_type, ", ".join(sorted(TEMPLATES.keys()))
            )
        )

    template_cls = TEMPLATES[bar_type]
    template = template_cls()
    output_dir = Path(output_dir)

    return template.generate(output_dir)


def dry_run(bar_type, output_dir):
    """Show what files would be generated without writing them.

    Args:
        bar_type: One of the registered template names.
        output_dir: The target directory (used for path display).

    Returns:
        List of relative path strings that would be created.

    Raises:
        ValueError: If bar_type is not recognized.
    """
    if bar_type not in TEMPLATES:
        raise ValueError(
            "Unknown bar type: '{}'. Available: {}".format(
                bar_type, ", ".join(sorted(TEMPLATES.keys()))
            )
        )

    # These are all the paths the base template writes
    paths = [
        "docs/inventory/beer.md",
        "docs/inventory/spirits.md",
        "docs/inventory/wine.md",
        "docs/vendors/README.md",
        "docs/menu/current.md",
        "docs/operations/opening.md",
        "docs/operations/closing.md",
        "docs/compliance/cooler-temps.md",
        "docs/compliance/pest-log.md",
        "docs/compliance/incidents.md",
        "docs/compliance/staff-certs.md",
        "docs/permits/README.md",
        "docs/calendar.md",
        "docs/schedule/README.md",
        "docs/schedule/current.md",
        "docs/schedule/staff.md",
        "data/close-out/README.md",
        "data/86/README.md",
    ]

    output_dir = Path(output_dir)
    return [str(output_dir / p) for p in paths]
