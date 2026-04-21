"""I/O helpers for Maya skills. All output and file reads go through here."""

import json
import os
import sys
import tempfile
from pathlib import Path

from . import MAYA_ROOT
from .result import Result


def emit(result: Result, fmt: str = "text") -> None:
    """Write the skill result to stdout in the requested format."""
    if fmt == "json":
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    else:
        sys.stdout.write(result["summary"] + "\n")
        for f in result.get("findings", []):
            sys.stdout.write(
                "  [{severity}] {code}: {message}\n".format(**f)
            )


def read_allowed_path(path: Path, allowlist_root: Path) -> Path | None:
    """Resolve path and return it if it exists and is within allowlist_root.

    Returns None if the file does not exist.
    Raises PermissionError if the resolved path escapes the allowlist root.
    """
    resolved = path.resolve(strict=False)
    root_resolved = allowlist_root.resolve(strict=False)
    if not resolved.is_relative_to(root_resolved):
        raise PermissionError(
            "Path escapes allowlist root: {path}".format(path=path)
        )
    if not resolved.is_file():
        return None
    return resolved


def write_allowed_path(path: Path, allowlist_root: Path) -> Path:
    """Resolve path and return it if within allowlist_root.

    Raises PermissionError if the resolved path escapes the allowlist root.
    Unlike read_allowed_path, does not check file existence (file may not exist yet).
    """
    resolved = path.resolve(strict=False)
    root_resolved = allowlist_root.resolve(strict=False)
    if not resolved.is_relative_to(root_resolved):
        raise PermissionError(
            "Path escapes allowlist root: {path}".format(path=path)
        )
    return resolved


def atomic_write_text(
    path: Path, content: str, allowlist_root: Path
) -> Path:
    """Write content to path atomically (via temp file + rename).

    Validates path is within allowlist_root before writing.
    Returns the resolved path on success.
    """
    resolved = write_allowed_path(path, allowlist_root)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(resolved.parent), suffix=".tmp"
    )
    try:
        os.write(fd, content.encode("utf-8"))
        os.close(fd)
        fd = -1
        os.rename(tmp_path, str(resolved))
    except BaseException:
        if fd >= 0:
            os.close(fd)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
    return resolved
