"""Entrypoint for python -m skills.schedule_view."""

from skills._lib.runner import run_skill
from skills.schedule_view import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--week-of", type=str, default=None)
    parser.add_argument("--schedule-dir", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
