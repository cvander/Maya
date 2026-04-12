"""eighty-six -- Manage the 86 list (unavailable items)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


_KNOWN_CATEGORIES = {
    "beer": [
        "ale", "lager", "ipa", "stout", "porter", "pilsner", "wheat",
        "sour", "saison", "hef", "keg", "draft", "tap",
    ],
    "wine": [
        "red", "white", "rose", "sparkling", "champagne", "prosecco",
        "cab", "merlot", "pinot", "chardonnay", "sauv", "zinfandel",
        "riesling", "malbec", "syrah", "shiraz", "tempranillo",
    ],
    "spirits": [
        "vodka", "gin", "rum", "tequila", "mezcal", "whiskey", "whisky",
        "bourbon", "scotch", "brandy", "cognac", "absinthe", "liqueur",
        "amaretto", "kahlua", "baileys", "vermouth", "bitters",
        "triple sec", "cointreau", "campari", "aperol",
    ],
}

_FILE_HEADER = "# 86 List\n\nLast updated: {timestamp}\n"
_TABLE_HEADER = (
    "| Item | Category | Time | Reason | Reported By |\n"
    "|------|----------|------|--------|-------------|"
)


def _infer_category(item_name: str, inventory_dir: Path) -> str:
    """Infer category from keyword matching or inventory files."""
    lower = item_name.lower()
    for cat, keywords in _KNOWN_CATEGORIES.items():
        for kw in keywords:
            if kw in lower:
                return cat

    # Check inventory files for the item name
    for fname in ("beer.md", "spirits.md", "wine.md"):
        fpath = inventory_dir / fname
        resolved = io.read_allowed_path(fpath, allowlist_root=inventory_dir.parent)
        if resolved is None:
            continue
        text = resolved.read_text(encoding="utf-8")
        if lower in text.lower():
            return Path(fname).stem

    return "other"


def _parse_86_table(text: str) -> list[dict[str, str]]:
    """Parse the 86 list markdown table into rows."""
    tables = md_table.parse_tables(text)
    if not tables:
        return []
    return tables[0]


def _build_file(rows: list[dict[str, str]], timestamp: str) -> str:
    """Build the full markdown file content from rows."""
    lines = [_FILE_HEADER.format(timestamp=timestamp), _TABLE_HEADER]
    for row in rows:
        lines.append(
            "| {item} | {category} | {time} | {reason} | {reported_by} |".format(
                item=row.get("item", ""),
                category=row.get("category", ""),
                time=row.get("time", ""),
                reason=row.get("reason", ""),
                reported_by=row.get("reported by", ""),
            )
        )
    return "\n".join(lines) + "\n"


def _get_data_dir(ctx: object) -> Path:
    """Get the data directory from args or default."""
    if hasattr(ctx.args, "data_dir") and ctx.args.data_dir:
        return Path(ctx.args.data_dir)
    return MAYA_ROOT / "data" / "86"


def _get_allowlist_root(ctx: object) -> Path:
    """Get the allowlist root for write operations.

    Always MAYA_ROOT — prevents --data-dir from making the check tautological.
    """
    return MAYA_ROOT


def _get_inventory_dir(ctx: object) -> Path:
    """Get inventory directory for category inference."""
    if ctx.args.inventory_dir:
        return Path(ctx.args.inventory_dir)
    return MAYA_ROOT / "docs" / "inventory"


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("eighty_six.started")

    data_dir = _get_data_dir(ctx)
    allowlist_root = _get_allowlist_root(ctx)
    file_path = data_dir / "current.md"
    inventory_dir = _get_inventory_dir(ctx)

    add_item = getattr(ctx.args, "add", None)
    remove_item = getattr(ctx.args, "remove", None)
    list_items = getattr(ctx.args, "list_items", False)

    # Default to list behavior if no action flags
    if not add_item and not remove_item:
        list_items = True

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    if add_item:
        return _handle_add(
            ctx, file_path, allowlist_root, inventory_dir,
            add_item, timestamp,
        )
    elif remove_item:
        return _handle_remove(
            ctx, file_path, allowlist_root, remove_item, timestamp,
        )
    else:
        return _handle_list(ctx, file_path, allowlist_root)


def _handle_list(ctx: object, file_path: Path, allowlist_root: Path) -> Result:
    """List currently 86'd items."""
    resolved = io.read_allowed_path(file_path, allowlist_root=allowlist_root)

    if resolved is None:
        log.event("eighty_six.list_empty")
        return {
            "skill": "eighty-six",
            "status": "ok",
            "summary": "All clear. No items on the 86 list.",
            "data": {"items": [], "count": 0},
            "findings": [],
            "metrics": {},
        }

    text = resolved.read_text(encoding="utf-8")
    rows = _parse_86_table(text)

    if not rows:
        log.event("eighty_six.list_empty")
        return {
            "skill": "eighty-six",
            "status": "ok",
            "summary": "All clear. No items on the 86 list.",
            "data": {"items": [], "count": 0},
            "findings": [],
            "metrics": {},
        }

    findings = [
        {
            "severity": "warn",
            "code": "CURRENTLY_86D",
            "subject": row.get("item", "unknown"),
            "message": "{item} ({category}) - 86'd since {time}: {reason}".format(
                item=row.get("item", "unknown"),
                category=row.get("category", "other"),
                time=row.get("time", "unknown"),
                reason=row.get("reason", "no reason given"),
            ),
        }
        for row in rows
    ]

    items_data = [
        {
            "item": row.get("item", ""),
            "category": row.get("category", ""),
            "time": row.get("time", ""),
            "reason": row.get("reason", ""),
            "reported_by": row.get("reported by", ""),
        }
        for row in rows
    ]

    summary = "{count} item(s) currently 86'd.".format(count=len(rows))
    log.event("eighty_six.listed", count=len(rows))

    return {
        "skill": "eighty-six",
        "status": "warn",
        "summary": summary,
        "data": {"items": items_data, "count": len(rows)},
        "findings": findings,
        "metrics": {},
    }


def _handle_add(
    ctx: object,
    file_path: Path,
    allowlist_root: Path,
    inventory_dir: Path,
    item_name: str,
    timestamp: str,
) -> Result:
    """Add an item to the 86 list."""
    reason = getattr(ctx.args, "reason", None) or "No reason given"
    reported_by = getattr(ctx.args, "reported_by", None) or "Unknown"

    category = _infer_category(item_name, inventory_dir)

    # Read existing file or start fresh
    resolved = io.read_allowed_path(file_path, allowlist_root=allowlist_root)
    if resolved is not None:
        text = resolved.read_text(encoding="utf-8")
        rows = _parse_86_table(text)
    else:
        rows = []

    # Check if item already exists (case-insensitive)
    for row in rows:
        if row.get("item", "").lower() == item_name.lower():
            log.event("eighty_six.add_duplicate", item_count=len(rows))
            return {
                "skill": "eighty-six",
                "status": "warn",
                "summary": "{item} is already on the 86 list.".format(item=item_name),
                "data": {"item": item_name, "action": "add", "duplicate": True},
                "findings": [
                    {
                        "severity": "info",
                        "code": "ITEM_86D",
                        "subject": item_name,
                        "message": "{item} was already 86'd.".format(item=item_name),
                    }
                ],
                "metrics": {},
            }

    new_row = {
        "item": item_name,
        "category": category,
        "time": timestamp,
        "reason": reason,
        "reported by": reported_by,
    }
    rows.append(new_row)

    content = _build_file(rows, timestamp)
    io.atomic_write_text(file_path, content, allowlist_root)

    log.event("eighty_six.added", item_count=len(rows))

    return {
        "skill": "eighty-six",
        "status": "ok",
        "summary": "{item} added to 86 list.".format(item=item_name),
        "data": {"item": item_name, "category": category, "action": "add"},
        "findings": [
            {
                "severity": "info",
                "code": "ITEM_86D",
                "subject": item_name,
                "message": "{item} 86'd: {reason} (reported by {by}).".format(
                    item=item_name, reason=reason, by=reported_by,
                ),
            }
        ],
        "metrics": {},
    }


def _handle_remove(
    ctx: object,
    file_path: Path,
    allowlist_root: Path,
    item_name: str,
    timestamp: str,
) -> Result:
    """Remove an item from the 86 list (back in stock)."""
    resolved = io.read_allowed_path(file_path, allowlist_root=allowlist_root)

    if resolved is None:
        log.event("eighty_six.remove_not_found", item_count=0)
        return {
            "skill": "eighty-six",
            "status": "ok",
            "summary": "{item} was not on the 86 list.".format(item=item_name),
            "data": {"item": item_name, "action": "remove", "found": False},
            "findings": [],
            "metrics": {},
        }

    text = resolved.read_text(encoding="utf-8")
    rows = _parse_86_table(text)

    original_count = len(rows)
    rows = [
        r for r in rows
        if r.get("item", "").lower() != item_name.lower()
    ]

    if len(rows) == original_count:
        log.event("eighty_six.remove_not_found", item_count=len(rows))
        return {
            "skill": "eighty-six",
            "status": "ok",
            "summary": "{item} was not on the 86 list.".format(item=item_name),
            "data": {"item": item_name, "action": "remove", "found": False},
            "findings": [],
            "metrics": {},
        }

    content = _build_file(rows, timestamp)
    io.atomic_write_text(file_path, content, allowlist_root)

    log.event("eighty_six.removed", item_count=len(rows))

    return {
        "skill": "eighty-six",
        "status": "ok",
        "summary": "{item} is back. Removed from 86 list.".format(item=item_name),
        "data": {"item": item_name, "action": "remove", "found": True},
        "findings": [
            {
                "severity": "info",
                "code": "ITEM_BACK",
                "subject": item_name,
                "message": "{item} back in stock.".format(item=item_name),
            }
        ],
        "metrics": {},
    }
