"""Entrypoint for python -m skills.schedule_notify."""

from skills._lib.runner import run_skill
from skills.schedule_notify import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--input-file", type=str, required=True)


run_skill(skill_module, extra_parser=_extra_args)
