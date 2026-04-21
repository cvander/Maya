"""Entrypoint for python -m skills.cost_analysis."""

from skills._lib.runner import run_skill
from skills.cost_analysis import main as skill_module


def _extra_args(parser):
    """Add cost-analysis specific CLI arguments."""
    parser.add_argument(
        "--category",
        type=str,
        default="all",
        choices=["all", "beer", "spirits", "wine", "cocktails"],
    )
    parser.add_argument("--menu-file", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
