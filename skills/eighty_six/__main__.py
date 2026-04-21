"""Entrypoint for python -m skills.eighty_six."""

from skills._lib.runner import run_skill
from skills.eighty_six import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--add", type=str, default=None)
    parser.add_argument("--remove", type=str, default=None)
    parser.add_argument("--reason", type=str, default=None)
    parser.add_argument("--reported-by", type=str, default=None)
    parser.add_argument("--list", action="store_true", dest="list_items")
    parser.add_argument("--data-dir", type=str, default=None)


run_skill(skill_module, extra_parser=_extra_args)
