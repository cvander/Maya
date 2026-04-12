"""Entrypoint for python -m skills.compliance_docs."""

from skills._lib.runner import run_skill
from skills.compliance_docs import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--compliance-dir", type=str, default=None,
                        help="Override compliance docs root (default: docs/compliance)")


run_skill(skill_module, extra_parser=_extra_args)
