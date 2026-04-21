"""schedule-notify -- Generate per-staff notification messages from a schedule."""

from __future__ import annotations

import json
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.result import Result


def _format_shift(shift: dict) -> str:
    """Format a single shift as a human-readable line."""
    return "{day} {start}-{end} ({role})".format(
        day=shift.get("day", ""),
        start=shift.get("start", ""),
        end=shift.get("end", ""),
        role=shift.get("role", ""),
    )


def _build_notifications(schedule_data: dict) -> list[dict]:
    """Group shifts by staff and build notification messages."""
    shifts = schedule_data.get("shifts", schedule_data.get("entries", []))
    week_of = schedule_data.get("week_of", "unknown")

    # Group shifts by staff name
    staff_shifts: dict[str, list[dict]] = {}
    for shift in shifts:
        name = shift.get("staff", "")
        if not name:
            continue
        if name not in staff_shifts:
            staff_shifts[name] = []
        staff_shifts[name].append(shift)

    notifications = []
    for name, person_shifts in sorted(staff_shifts.items()):
        lines = ["Schedule for week of {week}:".format(week=week_of), ""]
        for shift in person_shifts:
            lines.append("  {line}".format(line=_format_shift(shift)))
        total_hours = sum(s.get("hours", 0.0) for s in person_shifts)
        lines.append("")
        lines.append("Total: {hours:.1f}h".format(hours=total_hours))

        notifications.append({
            "staff": name,
            "shift_count": len(person_shifts),
            "total_hours": total_hours,
            "message": "\n".join(lines),
        })

    return notifications


def run(ctx: object) -> Result:
    """Parse schedule JSON and generate per-staff notifications."""
    input_file = ctx.args.input_file
    if not input_file:
        log.event("schedule_notify.no_input")
        return {
            "skill": "schedule-notify",
            "status": "fail",
            "summary": "No --input-file provided.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    input_path = Path(input_file)
    allowlist_root = input_path.parent

    log.event("schedule_notify.started")

    resolved = io.read_allowed_path(input_path, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("schedule_notify.file_missing", file=str(input_path))
        return {
            "skill": "schedule-notify",
            "status": "fail",
            "summary": "Input file not found: {path}".format(path=input_file),
            "data": {},
            "findings": [],
            "metrics": {},
        }

    raw = resolved.read_text(encoding="utf-8")
    try:
        schedule_json = json.loads(raw)
    except json.JSONDecodeError:
        log.event("schedule_notify.parse_error", file=str(input_path))
        return {
            "skill": "schedule-notify",
            "status": "fail",
            "summary": "Invalid JSON in input file.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    # Extract the schedule data (supports both schedule-view and schedule-draft output)
    schedule_data = schedule_json.get("data", schedule_json)

    notifications = _build_notifications(schedule_data)

    if not notifications:
        log.event("schedule_notify.no_staff")
        return {
            "skill": "schedule-notify",
            "status": "warn",
            "summary": "No staff shifts found in input.",
            "data": {"notifications": []},
            "findings": [],
            "metrics": {},
        }

    summary = "{count} notification(s) generated.".format(count=len(notifications))

    log.event(
        "schedule_notify.finished",
        notification_count=len(notifications),
    )

    return {
        "skill": "schedule-notify",
        "status": "ok",
        "summary": summary,
        "data": {"notifications": notifications},
        "findings": [],
        "metrics": {},
    }
