"""close-out-report -- Aggregate close-out data over a date range."""

from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.result import Result


def _today_str() -> str:
    """Return today's date as YYYY-MM-DD."""
    return date.today().isoformat()


def _parse_date(s: str) -> date | None:
    """Parse YYYY-MM-DD string to date, or None if invalid."""
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _extract_table_value(text: str, row_label: str) -> float | None:
    """Extract a dollar value from a markdown table row by label.

    Looks for patterns like '| Label | $123.45 |' or '| **Label** | **$123.45** |'.
    """
    pattern = r"\|\s*\*?\*?{label}\*?\*?\s*\|\s*\*?\*?\$([+-]?[\d,.]+)\*?\*?\s*\|".format(
        label=re.escape(row_label)
    )
    match = re.search(pattern, text)
    if match:
        val_str = match.group(1).replace(",", "")
        try:
            return float(val_str)
        except ValueError:
            return None
    return None


def _extract_variance(text: str) -> float | None:
    """Extract variance value, handling +/- prefix."""
    pattern = r"\|\s*\*?\*?Variance\*?\*?\s*\|\s*\*?\*?\$([+-]?[\d,.]+)\*?\*?\s*\|"
    match = re.search(pattern, text)
    if match:
        val_str = match.group(1).replace(",", "")
        try:
            return float(val_str)
        except ValueError:
            return None
    return None


def _extract_waste_items(text: str) -> list[str]:
    """Extract waste item names from the Waste table."""
    items = []
    in_waste = False
    past_separator = False
    for line in text.splitlines():
        if "## Waste" in line:
            in_waste = True
            past_separator = False
            continue
        if in_waste and line.startswith("##"):
            break
        if in_waste and re.match(r"\s*\|[-\s|]+\|\s*$", line):
            past_separator = True
            continue
        if in_waste and past_separator and "|" in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0] and not cells[0].startswith("-"):
                items.append(cells[0])
    return items


def _parse_close_out_file(text: str) -> dict | None:
    """Parse a close-out markdown file into structured data."""
    cash = _extract_table_value(text, "Cash")
    card = _extract_table_value(text, "Card")
    total = _extract_table_value(text, "Total")
    expected = _extract_table_value(text, "Expected")
    variance = _extract_variance(text)
    tip_total = _extract_table_value(text, "Total tips")
    staff_tips = _extract_table_value(text, "Staff (80%)")
    house_tips = _extract_table_value(text, "House (20%)")
    waste = _extract_waste_items(text)

    if total is None and (cash is not None and card is not None):
        total = cash + card

    if total is None:
        return None

    return {
        "cash": cash or 0.0,
        "card": card or 0.0,
        "total": total,
        "expected": expected or 0.0,
        "variance": variance or 0.0,
        "tip_total": tip_total or 0.0,
        "staff_tips": staff_tips or 0.0,
        "house_tips": house_tips or 0.0,
        "waste_items": waste,
    }


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("close_out_report.started")

    args = ctx.args
    data_dir_arg = args.data_dir
    if data_dir_arg:
        data_dir = Path(data_dir_arg)
    else:
        data_dir = MAYA_ROOT / "data" / "close-out"

    from_date = _parse_date(args.from_date) if args.from_date else None
    to_date = _parse_date(args.to_date) if args.to_date else None

    if args.from_date and from_date is None:
        log.event("close_out_report.bad_date", field="from")
        return {
            "skill": "close-out-report",
            "status": "fail",
            "summary": "Invalid --from date format. Use YYYY-MM-DD.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    if args.to_date and to_date is None:
        log.event("close_out_report.bad_date", field="to")
        return {
            "skill": "close-out-report",
            "status": "fail",
            "summary": "Invalid --to date format. Use YYYY-MM-DD.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    # Find all close-out files
    allowlist_root = data_dir
    md_files = sorted(data_dir.glob("*.md")) if data_dir.is_dir() else []

    days_data = []
    waste_counter: Counter = Counter()

    for fpath in md_files:
        # Extract date from filename
        stem = fpath.stem
        file_date = _parse_date(stem)
        if file_date is None:
            continue

        # Apply date range filter
        if from_date and file_date < from_date:
            continue
        if to_date and file_date > to_date:
            continue

        resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
        if resolved is None:
            continue

        text = resolved.read_text(encoding="utf-8")
        parsed = _parse_close_out_file(text)
        if parsed is None:
            log.event("close_out_report.parse_failed", file=fpath.name)
            continue

        parsed["date"] = stem
        days_data.append(parsed)

        for item in parsed["waste_items"]:
            waste_counter[item] += 1

    if not days_data:
        log.event("close_out_report.no_data")
        return {
            "skill": "close-out-report",
            "status": "ok",
            "summary": "No close-out data found in range.",
            "data": {"days": 0},
            "findings": [],
            "metrics": {},
        }

    # Aggregate
    total_revenue = sum(d["total"] for d in days_data)
    total_expected = sum(d["expected"] for d in days_data)
    total_variance = sum(d["variance"] for d in days_data)
    avg_variance = total_variance / len(days_data)
    total_tips = sum(d["tip_total"] for d in days_data)
    total_staff_tips = sum(d["staff_tips"] for d in days_data)
    total_house_tips = sum(d["house_tips"] for d in days_data)
    avg_daily_revenue = total_revenue / len(days_data)

    waste_freq = [
        {"item": item, "count": count}
        for item, count in waste_counter.most_common()
    ]

    data = {
        "days": len(days_data),
        "date_range": {
            "from": days_data[0]["date"],
            "to": days_data[-1]["date"],
        },
        "total_revenue": round(total_revenue, 2),
        "total_expected": round(total_expected, 2),
        "avg_daily_revenue": round(avg_daily_revenue, 2),
        "total_variance": round(total_variance, 2),
        "avg_variance": round(avg_variance, 2),
        "total_tips": round(total_tips, 2),
        "total_staff_tips": round(total_staff_tips, 2),
        "total_house_tips": round(total_house_tips, 2),
        "waste_frequency": waste_freq,
    }

    status = "ok"
    summary = "{days} day(s) analyzed: ${revenue:.2f} total revenue, avg variance ${avg_var:+.2f}.".format(
        days=len(days_data),
        revenue=total_revenue,
        avg_var=avg_variance,
    )

    log.event(
        "close_out_report.finished",
        days=len(days_data),
        total_revenue=round(total_revenue, 2),
    )

    return {
        "skill": "close-out-report",
        "status": status,
        "summary": summary,
        "data": data,
        "findings": [],
        "metrics": {},
    }
