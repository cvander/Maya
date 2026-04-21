"""Entrypoint for python -m skills.vendor_contact."""

from skills._lib.runner import run_skill
from skills.vendor_contact import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--vendor", type=str, default=None)
    parser.add_argument("--method", type=str, choices=["email", "phone"], default=None)


run_skill(skill_module, extra_parser=_extra_args)
