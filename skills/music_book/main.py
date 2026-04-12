"""music-book -- Generate outreach messages for booking artists."""

from __future__ import annotations

from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


def _find_artist(tables: list[list[dict[str, str]]], name: str) -> dict[str, str] | None:
    """Find an artist by case-insensitive name match across all tables."""
    name_lower = name.lower()
    for table in tables:
        for row in table:
            row_name = row.get("name", "").strip()
            if row_name.lower() == name_lower:
                return row
    return None


def _find_conflicts(
    tables: list[list[dict[str, str]]], artist_name: str, date: str,
) -> list[dict[str, str]]:
    """Find calendar entries that conflict on the given date."""
    conflicts = []
    for table in tables:
        for row in table:
            if row.get("date", "").strip() == date:
                conflicts.append(row)
    return conflicts


def _parse_rate(rate_str: str) -> str:
    """Return the rate string cleaned up."""
    return rate_str.strip()


def _generate_email(artist: dict[str, str], date: str) -> str:
    """Generate an email outreach message."""
    name = artist.get("name", "").strip()
    contact = artist.get("contact", "").strip()
    rate = artist.get("rate", "").strip()
    availability = artist.get("availability", "").strip()
    notes = artist.get("notes", "").strip()

    lines = [
        "Subject: Booking Inquiry - {date}".format(date=date),
        "",
        "Hi {name},".format(name=name),
        "",
        "We'd love to have you play at Maya's on {date}.".format(date=date),
        "",
        "Details:",
        "- Date: {date}".format(date=date),
        "- Your rate: {rate}".format(rate=rate),
        "- Venue: Maya's Bar, San Francisco",
    ]
    if notes:
        lines.append("- Notes: {notes}".format(notes=notes))
    lines.extend([
        "",
        "Let us know if this works for you.",
        "",
        "Best,",
        "Maya",
    ])
    return "\n".join(lines)


def _generate_phone_script(artist: dict[str, str], date: str) -> str:
    """Generate a phone call script."""
    name = artist.get("name", "").strip()
    rate = artist.get("rate", "").strip()
    notes = artist.get("notes", "").strip()

    lines = [
        "PHONE SCRIPT",
        "============",
        "",
        "Call: {name}".format(name=name),
        "",
        "Hi, this is Maya's Bar in San Francisco.",
        "We're looking to book you for {date}.".format(date=date),
        "Your usual rate is {rate} - does that still work?".format(rate=rate),
    ]
    if notes:
        lines.append("Note: {notes}".format(notes=notes))
    lines.extend([
        "",
        "Confirm date, time, and any equipment needs.",
    ])
    return "\n".join(lines)


def run(ctx: object) -> Result:
    """Main skill entry point."""
    music_dir = ctx.args.music_dir or (MAYA_ROOT / "docs" / "music")
    music_dir = Path(music_dir)
    artist_name = ctx.args.artist
    date = ctx.args.date
    method = ctx.args.method

    if ctx.args.music_dir:
        allowlist_root = music_dir
    else:
        allowlist_root = MAYA_ROOT / "docs"

    log.event("music_book.started", method=method)

    # Read artists file
    artists_path = music_dir / "artists.md"
    resolved = io.read_allowed_path(artists_path, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("music_book.file_missing", file="artists.md")
        return {
            "skill": "music-book",
            "status": "fail",
            "summary": "Artists file not found.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    artists_text = resolved.read_text(encoding="utf-8")
    artist_tables = md_table.parse_tables(artists_text)

    # Find the artist
    artist = _find_artist(artist_tables, artist_name)
    if artist is None:
        log.event("music_book.artist_not_found", searched=artist_name)
        return {
            "skill": "music-book",
            "status": "warn",
            "summary": "Artist not found: {name}.".format(name=artist_name),
            "data": {"artist_info": None, "message": None, "conflict": None},
            "findings": [
                {
                    "severity": "warn",
                    "code": "ARTIST_NOT_FOUND",
                    "subject": artist_name,
                    "message": "Artist not found in directory: {name}.".format(
                        name=artist_name
                    ),
                }
            ],
            "metrics": {},
        }

    # Build artist info dict
    artist_info = {
        "name": artist.get("name", "").strip(),
        "genre": artist.get("genre", "").strip(),
        "contact": artist.get("contact", "").strip(),
        "rate": artist.get("rate", "").strip(),
        "availability": artist.get("availability", "").strip(),
        "notes": artist.get("notes", "").strip(),
    }

    # Check calendar for conflicts
    conflict = None
    calendar_path = music_dir / "calendar.md"
    cal_resolved = io.read_allowed_path(calendar_path, allowlist_root=allowlist_root)
    if cal_resolved is not None:
        cal_text = cal_resolved.read_text(encoding="utf-8")
        cal_tables = md_table.parse_tables(cal_text)
        conflicts = _find_conflicts(cal_tables, artist_name, date)
        if conflicts:
            conflict = {
                "date": date,
                "existing": [
                    {
                        "artist": c.get("artist", "").strip(),
                        "time": c.get("time", "").strip(),
                        "status": c.get("status", "").strip(),
                    }
                    for c in conflicts
                ],
            }

    # Generate outreach message
    if method == "email":
        message = _generate_email(artist, date)
    else:
        message = _generate_phone_script(artist, date)

    findings = []

    if conflict:
        findings.append({
            "severity": "warn",
            "code": "DATE_CONFLICT",
            "subject": date,
            "message": "Date {date} already has booking(s): {artists}.".format(
                date=date,
                artists=", ".join(
                    e["artist"] for e in conflict["existing"]
                ),
            ),
        })

    findings.append({
        "severity": "info",
        "code": "BOOKING_DRAFT",
        "subject": artist_info["name"],
        "message": "Outreach message generated via {method}.".format(method=method),
    })

    status = "warn" if conflict else "ok"
    if conflict:
        summary = "Booking draft ready for {name} on {date} (date conflict found).".format(
            name=artist_info["name"], date=date
        )
    else:
        summary = "Booking draft ready for {name} on {date}.".format(
            name=artist_info["name"], date=date
        )

    log.event(
        "music_book.finished",
        artist=artist_info["name"],
        has_conflict=conflict is not None,
    )

    return {
        "skill": "music-book",
        "status": status,
        "summary": summary,
        "data": {
            "artist_info": artist_info,
            "message": message,
            "conflict": conflict,
        },
        "findings": findings,
        "metrics": {},
    }
