"""Entrypoint for python -m skills.music_book."""

from skills._lib.runner import run_skill
from skills.music_book import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--artist", required=True, help="Artist name to book.")
    parser.add_argument("--date", required=True, help="Date to book (YYYY-MM-DD).")
    parser.add_argument(
        "--method", choices=["email", "phone"], default="email",
        help="Outreach method.",
    )
    parser.add_argument(
        "--music-dir", default=None,
        help="Override music data directory (default: docs/music).",
    )


run_skill(skill_module, extra_parser=_extra_args)
