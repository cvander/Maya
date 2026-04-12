"""Entrypoint for python -m skills.vendor_order."""

from skills._lib.runner import run_skill
from skills.vendor_order import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--vendor", type=str, default=None)
    parser.add_argument("--input-file", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
