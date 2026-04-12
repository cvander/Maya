"""Skill runner: loads manifest, parses args, calls run(), emits result."""

import argparse
import json
import sys
import time
import tomllib
from pathlib import Path

from . import MAYA_ROOT
from . import io as skill_io
from . import log
from .result import ExitCode, Result


def run_skill(
    skill_module: object,
    argv: list[str] | None = None,
    extra_parser: object | None = None,
) -> None:
    """Run a skill module through the standard pipeline.

    1. Parse shared CLI args.
    2. Load the skill's manifest.toml.
    3. Call skill_module.run(ctx).
    4. Emit result, set exit code.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        dest="output_format",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--inventory-dir", type=Path, default=None)

    if extra_parser:
        extra_parser(parser)

    args = parser.parse_args(argv)

    # Load manifest
    skill_dir = Path(skill_module.__file__).resolve().parent
    manifest_path = skill_dir / "manifest.toml"
    try:
        with manifest_path.open("rb") as f:
            manifest = tomllib.load(f)
    except (FileNotFoundError, tomllib.TOMLDecodeError) as exc:
        err_result: Result = {
            "skill": "unknown",
            "status": "fail",
            "summary": "Could not load manifest.",
            "data": {},
            "findings": [],
            "metrics": {"duration_ms": 0},
        }
        skill_io.emit(err_result, args.output_format)
        sys.exit(ExitCode.CONFIG_ERROR)

    skill_name = manifest.get("skill", {}).get("name", "unknown")

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.args = args
    ctx.manifest = manifest

    start = time.monotonic()
    try:
        result = skill_module.run(ctx)
    except Exception:
        duration_ms = int((time.monotonic() - start) * 1000)
        log.event(
            "{name}.error".format(name=skill_name.replace("-", "_")),
            exit_code=ExitCode.UNEXPECTED,
        )
        err_result = {
            "skill": skill_name,
            "status": "fail",
            "summary": "Unexpected error.",
            "data": {},
            "findings": [],
            "metrics": {"duration_ms": duration_ms},
        }
        skill_io.emit(err_result, args.output_format)
        sys.exit(ExitCode.UNEXPECTED)

    duration_ms = int((time.monotonic() - start) * 1000)
    result["metrics"] = {"duration_ms": duration_ms}

    skill_io.emit(result, args.output_format)

    status = result.get("status", "fail")
    if status == "ok":
        sys.exit(ExitCode.OK)
    elif status == "warn":
        sys.exit(ExitCode.WARN)
    else:
        sys.exit(ExitCode.DATA_ERROR)
