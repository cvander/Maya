"""music-calendar -- View and filter the music booking calendar."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


def _parse_date(date_str: str) -> date | None:
    """Parse a YYYY-MM-DD date string, return None on failure."""
    try:
        return date.fromisoformat(date_str.strip())
    except (ValueError, AttributeError):
        return None


def _parse_fee(fee_str: str) -> int:
    """Parse a fee string like '$300' into an integer. Returns 0 on failure."""
    cleaned = fee_str.strip().replace("$", "").replace(",", "")
    try:
        return int(cleaned)
    except (ValueError, AttributeError):
        return 0


def run(ctx: object) -> Result:
    """Main skill entry point."""
    music_dir = ctx.args.music_dir or (MAYA_ROOT / "docs" / "music")
    music_dir = Path(music_dir)

    if ctx.args.music_dir:
        allowlist_root = music_dir
    else:
        allowlist_root = MAYA_ROOT / "docs"

    log.event("music_calendar.started")

    # Read calendar file
    calendar_path = music_dir / "calendar.md"
    resolved = io.read_allowed_path(calendar_path, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("music_calendar.file_missing", file="calendar.md")
        return {
            "skill": "music-calendar",
            "status": "fail",
            "summary": "Calendar file not found.",
            "data": {"events": [], "total_fees": 0},
            "findings": [],
            "metrics": {},
        }

    cal_text = resolved.read_text(encoding="utf-8")
    cal_tables = md_table.parse_tables(cal_text)

    # Determine date range
    from_date = None
    to_date = None

    if ctx.args.from_date:
        from_date = _parse_date(ctx.args.from_date)
    if ctx.args.to_date:
        to_date = _parse_date(ctx.args.to_date)

    if from_date is None and to_date is None:
        from_date = date.today()
        to_date = from_date + timedelta(weeks=ctx.args.weeks)
    elif from_date is not None and to_date is None:
        to_date = from_date + timedelta(weeks=ctx.args.weeks)
    elif from_date is None and to_date is not None:
        from_date = date.today()

    status_filter = ctx.args.status

    # Parse and filter events
    events = []
    for table in cal_tables:
        for row in table:
            event_date = _parse_date(row.get("date", ""))
            if event_date is None:
                continue

            if event_date < from_date or event_date > to_date:
                continue

            event_status = row.get("status", "").strip().lower()
            if status_filter != "all" and event_status != status_filter:
                continue

            events.append({
                "date": row.get("date", "").strip(),
                "artist": row.get("artist", "").strip(),
                "time": row.get("time", "").strip(),
                "genre": row.get("genre", "").strip(),
                "fee": row.get("fee", "").strip(),
                "status": event_status,
            })

    # Sort by date
    events.sort(key=lambda e: e["date"])

    # Calculate total fees
    total_fees = sum(_parse_fee(e["fee"]) for e in events)

    log.event(
        "music_calendar.parsed",
        event_count=len(events),
        total_fees=total_fees,
    )

    status = "ok"
    if not events:
        summary = "No events found in the specified range."
    else:
        summary = "{count} event(s) found, total fees: ${fees}.".format(
            count=len(events), fees=total_fees
        )

    findings = []
    for e in events:
        findings.append({
            "severity": "info",
            "code": "EVENT",
            "subject": "{date}/{artist}".format(date=e["date"], artist=e["artist"]),
            "message": "{artist} on {date} ({status}) - {fee}.".format(
                artist=e["artist"], date=e["date"],
                status=e["status"], fee=e["fee"],
            ),
        })

    log.event(
        "music_calendar.finished",
        event_count=len(events),
        total_fees=total_fees,
    )

    return {
        "skill": "music-calendar",
        "status": status,
        "summary": summary,
        "data": {"events": events, "total_fees": total_fees},
        "findings": findings,
        "metrics": {},
    }
