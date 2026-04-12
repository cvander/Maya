"""inventory-check skill logic."""

from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


_FILES = ["beer.md", "spirits.md", "wine.md"]


def _parse_int(value: str | None) -> int | None:
    """Return an int if value is a non-empty integer string, else None."""
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return int(stripped)
    except ValueError:
        return None


def _category_from_filename(fname: str) -> str:
    """Derive category from filename stem: beer.md -> beer."""
    return Path(fname).stem


def _item_label(row: dict[str, str]) -> str:
    """Pick the best item label from a row."""
    for key in ("brand", "beer", "producer", "item", "wine"):
        val = row.get(key, "").strip()
        if val:
            return val
    # Composite fallback: join all non-empty values
    parts = [v.strip() for v in row.values() if v.strip()]
    return parts[0] if parts else "unknown"


def run(ctx: object) -> Result:
    """Scan inventory files for items at or below reorder threshold."""
    inventory_dir = ctx.args.inventory_dir or (MAYA_ROOT / "docs" / "inventory")
    inventory_dir = Path(inventory_dir)

    # Determine allowlist root based on inventory_dir
    if ctx.args.inventory_dir:
        allowlist_root = inventory_dir
    else:
        allowlist_root = MAYA_ROOT / "docs"

    log.event("inventory_check.started")

    items_scanned = 0
    low_stock: list[dict] = []

    for fname in _FILES:
        fpath = inventory_dir / fname
        resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
        if resolved is None:
            log.event("inventory_check.file_missing", file=fname)
            continue

        text = resolved.read_text(encoding="utf-8")
        row_count = 0
        for table in md_table.parse_tables(text):
            for row in table:
                qty = _parse_int(row.get("qty") or row.get("qty (kegs)"))
                threshold = _parse_int(row.get("reorder at"))
                if qty is None or threshold is None:
                    continue
                items_scanned += 1
                row_count += 1
                if qty <= threshold:
                    low_stock.append({
                        "category": _category_from_filename(fname),
                        "item": _item_label(row),
                        "qty": qty,
                        "reorder_at": threshold,
                    })

        log.event("inventory_check.file_read", file=fname, row_count=row_count)

    status = "warn" if low_stock else "ok"
    if low_stock:
        summary = "{count} item(s) at or below reorder threshold.".format(
            count=len(low_stock)
        )
    else:
        summary = "{count} item(s) checked. Nothing to reorder.".format(
            count=items_scanned
        )

    findings = [
        {
            "severity": "warn",
            "code": "LOW_STOCK",
            "subject": "{cat}/{item}".format(cat=i["category"], item=i["item"]),
            "message": "{item}: {qty} on hand, reorder at {reorder_at}.".format(**i),
        }
        for i in low_stock
    ]

    log.event(
        "inventory_check.finished",
        items_scanned=items_scanned,
        low_stock_count=len(low_stock),
    )

    return {
        "skill": "inventory-check",
        "status": status,
        "summary": summary,
        "data": {"items_scanned": items_scanned, "low_stock": low_stock},
        "findings": findings,
        "metrics": {},
    }
