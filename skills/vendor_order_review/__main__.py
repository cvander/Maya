"""Entrypoint for python -m skills.vendor_order_review."""

from skills._lib.runner import run_skill
from skills.vendor_order_review import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--input-file", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
