"""Entrypoint for python -m skills.<skill_name>."""

from skills._lib.runner import run_skill
from skills._skeleton import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    # parser.add_argument("--custom-flag", default=None)
    pass


run_skill(skill_module, extra_parser=_extra_args)
