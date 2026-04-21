"""Shared helper for --dry-run support in Maya skills."""

import tempfile
from pathlib import Path

from skills._lib import MAYA_ROOT


def resolve_data_dir(ctx, default_subdir):
    """If --dry-run, return temp dir. Otherwise return real dir.

    Args:
        ctx: An object with an `args` attribute (e.g. argparse namespace).
             Checks for `ctx.args.dry_run` boolean.
        default_subdir: The subdirectory under MAYA_ROOT to use (e.g. 'data/86').

    Returns:
        Path to the resolved directory.
    """
    if getattr(getattr(ctx, 'args', None), 'dry_run', False):
        return Path(tempfile.mkdtemp()) / default_subdir
    return MAYA_ROOT / default_subdir
