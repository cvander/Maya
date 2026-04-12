"""Entrypoint for python -m skills.compliance_check."""

from skills._lib.runner import run_skill
from skills.compliance_check import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--date", type=str, default=None,
                        help="Override today's date (YYYY-MM-DD)")
    parser.add_argument("--days-ahead", type=int, default=30,
                        help="Look-ahead window in days (default: 30)")
    parser.add_argument("--compliance-dir", type=str, default=None,
                        help="Override compliance docs root (default: docs/compliance)")


run_skill(skill_module, extra_parser=_extra_args)
