"""Entrypoint for python -m skills.close_out."""

from skills._lib.runner import run_skill
from skills.close_out import main as skill_module


def _extra_args(parser):
    """Add close-out specific CLI arguments."""
    parser.add_argument("--date", type=str, default=None)
    parser.add_argument("--cash-count", type=float, default=None)
    parser.add_argument("--card-total", type=float, default=None)
    parser.add_argument("--expected", type=float, default=None)
    parser.add_argument("--tip-total", type=float, default=None)
    parser.add_argument("--waste-items", type=str, default=None)
    parser.add_argument("--data-dir", type=str, default=None)
    parser.add_argument("--force", action="store_true", default=False)


run_skill(skill_module, extra_parser=_extra_args)
