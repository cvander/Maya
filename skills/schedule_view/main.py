"""schedule-view -- Display the current weekly staff schedule."""

from __future__ import annotations

from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


def _parse_schedule_table(text: str) -> list[dict[str, str]]:
    """Parse the schedule markdown table into a list of row dicts."""
    tables = md_table.parse_tables(text)
    if not tables:
        return []
    return tables[0]


def _extract_week_from_header(text: str) -> str | None:
    """Extract 'Week of YYYY-MM-DD' date from the schedule header."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and "week of" in stripped.lower():
            parts = stripped.split("Week of")
            if len(parts) == 2:
                return parts[1].strip()
            parts = stripped.split("week of")
            if len(parts) == 2:
                return parts[1].strip()
    return None


def _calc_hours(start: str, end: str) -> float:
    """Calculate shift duration in hours from HH:MM strings."""
    try:
        sh, sm = int(start.split(":")[0]), int(start.split(":")[1])
        eh, em = int(end.split(":")[0]), int(end.split(":")[1])
        start_min = sh * 60 + sm
        end_min = eh * 60 + em
        if end_min <= start_min:
            end_min += 24 * 60
        return (end_min - start_min) / 60.0
    except (ValueError, IndexError):
        return 0.0


def run(ctx: object) -> Result:
    """Read and display the weekly schedule."""
    schedule_dir = ctx.args.schedule_dir or (MAYA_ROOT / "docs" / "schedule")
    schedule_dir = Path(schedule_dir)

    if ctx.args.schedule_dir:
        allowlist_root = schedule_dir
    else:
        allowlist_root = MAYA_ROOT / "docs"

    log.event("schedule_view.started")

    current_path = schedule_dir / "current.md"
    resolved = io.read_allowed_path(current_path, allowlist_root=allowlist_root)

    if resolved is None:
        log.event("schedule_view.file_missing", file="current.md")
        return {
            "skill": "schedule-view",
            "status": "fail",
            "summary": "Schedule file not found: current.md",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    text = resolved.read_text(encoding="utf-8")
    week_of = _extract_week_from_header(text)
    entries = _parse_schedule_table(text)

    if not entries:
        log.event("schedule_view.empty_schedule")
        return {
            "skill": "schedule-view",
            "status": "warn",
            "summary": "No schedule entries found.",
            "data": {"week_of": week_of, "entries": [], "staff_hours": {}},
            "findings": [],
            "metrics": {},
        }

    # Filter by --week-of if provided (match against header)
    requested_week = getattr(ctx.args, "week_of", None)
    if requested_week and week_of and requested_week != week_of:
        log.event("schedule_view.week_mismatch", requested=requested_week, found=week_of)

    # Build structured entries
    parsed_entries = []
    staff_hours: dict[str, float] = {}
    for row in entries:
        entry = {
            "day": row.get("day", ""),
            "shift": row.get("shift", ""),
            "start": row.get("start", ""),
            "end": row.get("end", ""),
            "staff": row.get("staff", ""),
            "role": row.get("role", ""),
        }
        hours = _calc_hours(entry["start"], entry["end"])
        entry["hours"] = hours
        parsed_entries.append(entry)

        name = entry["staff"]
        if name:
            staff_hours[name] = staff_hours.get(name, 0.0) + hours

    summary = "{count} shift(s) scheduled for week of {week}.".format(
        count=len(parsed_entries),
        week=week_of or "unknown",
    )

    log.event(
        "schedule_view.finished",
        entry_count=len(parsed_entries),
        staff_count=len(staff_hours),
    )

    return {
        "skill": "schedule-view",
        "status": "ok",
        "summary": summary,
        "data": {
            "week_of": week_of,
            "entries": parsed_entries,
            "staff_hours": staff_hours,
        },
        "findings": [],
        "metrics": {},
    }
