"""schedule-draft -- Generate a draft weekly schedule with labor law checks."""

from __future__ import annotations

import datetime
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


_DAYS_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

_AVAILABILITY_MAP = {
    "Mon-Sat": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    "Tue-Sun": ["Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Mon-Fri": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "Wed-Sat": ["Wed", "Thu", "Fri", "Sat"],
    "Mon-Sun": _DAYS_ORDER[:],
}


def _parse_availability(avail_str: str) -> list[str]:
    """Parse availability string into list of day abbreviations."""
    avail_str = avail_str.strip()
    if avail_str in _AVAILABILITY_MAP:
        return _AVAILABILITY_MAP[avail_str]
    # Try individual days
    return [d.strip() for d in avail_str.split(",") if d.strip()]


def _parse_max_hours(value: str) -> int:
    """Parse max hours/week string to int."""
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return 40


def _parse_staff_table(text: str) -> list[dict]:
    """Parse staff.md into structured staff records."""
    tables = md_table.parse_tables(text)
    if not tables:
        return []
    staff = []
    for row in tables[0]:
        staff.append({
            "name": row.get("name", "").strip(),
            "role": row.get("role", "").strip(),
            "max_hours": _parse_max_hours(row.get("max hours/week", "40")),
            "availability": _parse_availability(row.get("availability", "")),
            "rbs_cert": row.get("rbs cert", "").strip().lower() == "yes",
            "rbs_expiry": row.get("rbs expiry", "").strip(),
        })
    return staff


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


def _get_week_monday(week_of: str | None) -> datetime.date:
    """Return the Monday of the requested week, or next Monday."""
    if week_of:
        try:
            d = datetime.date.fromisoformat(week_of)
            # Find the Monday of that week
            return d - datetime.timedelta(days=d.weekday())
        except ValueError:
            pass
    # Default: next Monday
    today = datetime.date.today()
    days_ahead = 7 - today.weekday()
    if days_ahead == 7:
        days_ahead = 7
    return today + datetime.timedelta(days=days_ahead)


def _is_rbs_valid(expiry_str: str, check_date: datetime.date) -> bool:
    """Check if RBS certification is valid on the given date."""
    if not expiry_str or expiry_str.strip() == "--":
        return False
    try:
        expiry = datetime.date.fromisoformat(expiry_str.strip())
        return expiry >= check_date
    except ValueError:
        return False


def _generate_draft(staff: list[dict], week_monday: datetime.date) -> list[dict]:
    """Generate a draft schedule assigning staff to days based on availability."""
    shifts = []
    bartenders = [s for s in staff if s["role"].lower() == "bartender"]
    barbacks = [s for s in staff if s["role"].lower() == "barback"]

    staff_hours: dict[str, float] = {s["name"]: 0.0 for s in staff}

    for day in _DAYS_ORDER:
        is_weekend = day in ("Sat", "Sun")
        start_time = "14:00" if is_weekend else "16:00"
        end_time = "02:00" if day in ("Thu", "Fri", "Sat") else ("22:00" if day == "Sun" else "00:00")
        shift_hours = _calc_hours(start_time, end_time)

        # Assign bartender (pick available one with fewest hours so far)
        available_bt = [
            b for b in bartenders
            if day in b["availability"] and staff_hours[b["name"]] + shift_hours <= b["max_hours"]
        ]
        available_bt.sort(key=lambda b: staff_hours[b["name"]])
        if available_bt:
            bt = available_bt[0]
            shifts.append({
                "day": day,
                "shift": "Open",
                "start": start_time,
                "end": end_time,
                "staff": bt["name"],
                "role": "Bartender",
                "hours": shift_hours,
            })
            staff_hours[bt["name"]] += shift_hours

        # Assign barback
        available_bb = [
            b for b in barbacks
            if day in b["availability"] and staff_hours[b["name"]] + shift_hours <= b["max_hours"]
        ]
        available_bb.sort(key=lambda b: staff_hours[b["name"]])
        if available_bb:
            bb = available_bb[0]
            shifts.append({
                "day": day,
                "shift": "Open",
                "start": start_time,
                "end": end_time,
                "staff": bb["name"],
                "role": "Barback",
                "hours": shift_hours,
            })
            staff_hours[bb["name"]] += shift_hours

    return shifts


def _check_labor_laws(shifts: list[dict], staff: list[dict], week_monday: datetime.date) -> list[dict]:
    """Check schedule against labor law requirements."""
    findings = []
    staff_map = {s["name"]: s for s in staff}

    # Accumulate hours per staff per day and per week
    daily_hours: dict[str, dict[str, float]] = {}
    weekly_hours: dict[str, float] = {}

    for shift in shifts:
        name = shift["staff"]
        day = shift["day"]
        hours = shift["hours"]
        if name not in daily_hours:
            daily_hours[name] = {}
        daily_hours[name][day] = daily_hours[name].get(day, 0.0) + hours
        weekly_hours[name] = weekly_hours.get(name, 0.0) + hours

    # OVERTIME_RISK: >8hrs/day or >40hrs/week (CA law)
    for name, days in daily_hours.items():
        for day, hours in days.items():
            if hours > 8:
                findings.append({
                    "severity": "warn",
                    "code": "OVERTIME_RISK",
                    "subject": name,
                    "message": "{name} scheduled {hours:.1f}h on {day} (>8h CA daily limit).".format(
                        name=name, hours=hours, day=day,
                    ),
                })

    for name, hours in weekly_hours.items():
        if hours > 40:
            findings.append({
                "severity": "warn",
                "code": "OVERTIME_RISK",
                "subject": name,
                "message": "{name} scheduled {hours:.1f}h/week (>40h CA weekly limit).".format(
                    name=name, hours=hours,
                ),
            })

    # PREDICTIVE_SCHED: schedule changes <7 days advance (SF ordinance)
    days_advance = (week_monday - datetime.date.today()).days
    if days_advance < 7:
        findings.append({
            "severity": "warn",
            "code": "PREDICTIVE_SCHED",
            "subject": "schedule",
            "message": "Schedule for {date} is only {days} day(s) in advance (SF requires 7).".format(
                date=week_monday.isoformat(), days=max(0, days_advance),
            ),
        })

    # MISSING_CERT: bartender shift without valid RBS cert
    for shift in shifts:
        if shift["role"].lower() == "bartender":
            staff_info = staff_map.get(shift["staff"])
            if staff_info and not staff_info["rbs_cert"]:
                findings.append({
                    "severity": "warn",
                    "code": "MISSING_CERT",
                    "subject": shift["staff"],
                    "message": "{name} assigned bartender shift on {day} without RBS certification.".format(
                        name=shift["staff"], day=shift["day"],
                    ),
                })
            elif staff_info and staff_info["rbs_cert"]:
                if not _is_rbs_valid(staff_info["rbs_expiry"], week_monday):
                    findings.append({
                        "severity": "warn",
                        "code": "MISSING_CERT",
                        "subject": shift["staff"],
                        "message": "{name} RBS cert expired before {date}.".format(
                            name=shift["staff"], date=week_monday.isoformat(),
                        ),
                    })

    return findings


def run(ctx: object) -> Result:
    """Generate a draft schedule and check labor law compliance."""
    schedule_dir = ctx.args.schedule_dir or (MAYA_ROOT / "docs" / "schedule")
    schedule_dir = Path(schedule_dir)

    if ctx.args.schedule_dir:
        allowlist_root = schedule_dir
    else:
        allowlist_root = MAYA_ROOT / "docs"

    log.event("schedule_draft.started")

    # Read staff data
    staff_path = schedule_dir / "staff.md"
    resolved_staff = io.read_allowed_path(staff_path, allowlist_root=allowlist_root)
    if resolved_staff is None:
        log.event("schedule_draft.file_missing", file="staff.md")
        return {
            "skill": "schedule-draft",
            "status": "fail",
            "summary": "Staff file not found: staff.md",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    staff_text = resolved_staff.read_text(encoding="utf-8")
    staff = _parse_staff_table(staff_text)

    if not staff:
        log.event("schedule_draft.no_staff")
        return {
            "skill": "schedule-draft",
            "status": "fail",
            "summary": "No staff records found in staff.md.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    # Determine target week
    week_of = getattr(ctx.args, "week_of", None)
    week_monday = _get_week_monday(week_of)

    # Read calendar for events (optional, always from MAYA_ROOT/docs)
    calendar_path = MAYA_ROOT / "docs" / "calendar.md"
    cal_allowlist = MAYA_ROOT / "docs"
    resolved_cal = io.read_allowed_path(calendar_path, allowlist_root=cal_allowlist)
    events_note = None
    if resolved_cal:
        cal_text = resolved_cal.read_text(encoding="utf-8")
        cal_tables = md_table.parse_tables(cal_text)
        # Check if any event falls in the target week
        for table in cal_tables:
            for row in table:
                event_str = row.get("event", "").strip()
                impact = row.get("impact", "").strip()
                if event_str and impact:
                    events_note = "Calendar events found. Review docs/calendar.md for staffing impact."
                    break

    # Generate draft
    shifts = _generate_draft(staff, week_monday)

    # Check labor laws
    findings = _check_labor_laws(shifts, staff, week_monday)

    # Build weekly hours summary
    weekly_hours: dict[str, float] = {}
    for shift in shifts:
        name = shift["staff"]
        weekly_hours[name] = weekly_hours.get(name, 0.0) + shift["hours"]

    status = "warn" if findings else "ok"
    summary = "Draft: {count} shift(s) for week of {week}, {findings} finding(s).".format(
        count=len(shifts),
        week=week_monday.isoformat(),
        findings=len(findings),
    )

    data = {
        "week_of": week_monday.isoformat(),
        "shifts": shifts,
        "staff_hours": weekly_hours,
    }
    if events_note:
        data["events_note"] = events_note

    log.event(
        "schedule_draft.finished",
        shift_count=len(shifts),
        findings_count=len(findings),
    )

    return {
        "skill": "schedule-draft",
        "status": status,
        "summary": summary,
        "data": data,
        "findings": findings,
        "metrics": {},
    }
