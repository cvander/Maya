"""Entrypoint for python -m skills.music_calendar."""

from skills._lib.runner import run_skill
from skills.music_calendar import main as skill_module


def _extra_args(parser):
    """Add skill-specific CLI arguments."""
    parser.add_argument("--from", dest="from_date", default=None,
                        help="Start date (YYYY-MM-DD).")
    parser.add_argument("--to", dest="to_date", default=None,
                        help="End date (YYYY-MM-DD).")
    parser.add_argument("--weeks", type=int, default=4,
                        help="Number of weeks to look ahead (default: 4).")
    parser.add_argument("--status", choices=["all", "confirmed", "tentative", "pending"],
                        default="all", help="Filter by booking status.")
    parser.add_argument("--music-dir", default=None,
                        help="Override music data directory (default: docs/music).")


run_skill(skill_module, extra_parser=_extra_args)
