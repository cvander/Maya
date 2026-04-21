"""Entrypoint for python -m skills.close_out_report."""

from skills._lib.runner import run_skill
from skills.close_out_report import main as skill_module


def _extra_args(parser):
    """Add close-out-report specific CLI arguments."""
    parser.add_argument("--from", type=str, default=None, dest="from_date")
    parser.add_argument("--to", type=str, default=None, dest="to_date")
    parser.add_argument("--data-dir", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
