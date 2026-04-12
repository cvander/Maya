"""vendor-order-review -- Parse inventory-check output and generate vendor orders."""

from __future__ import annotations

import json
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.md_table import parse_tables
from skills._lib.result import Result


# Map categories/items to vendors based on vendor docs.
# This is a simplified lookup; real implementation would parse vendors.md dynamically.


def _load_vendor_map(vendors_path: Path, allowlist_root: Path) -> dict[str, str]:
    """Parse vendors README to build item-category -> vendor mapping.

    Reads the Distributors table and builds a mapping from keywords in the
    Notes column to vendor names.
    """
    resolved = io.read_allowed_path(vendors_path, allowlist_root=allowlist_root)
    if resolved is None:
        return {}

    text = resolved.read_text(encoding="utf-8")
    tables = parse_tables(text)

    vendor_map: dict[str, str] = {}
    for table in tables:
        for row in table:
            vendor = row.get("vendor", "").strip()
            notes = row.get("notes", "").strip().lower()
            if not vendor:
                continue
            # Extract category keywords from notes.
            # First match wins (main distributor listed first).
            if ("spirits" in notes or "well" in notes or "call" in notes) and "spirits" not in vendor_map:
                vendor_map["spirits"] = vendor
            if "wine" in notes and "wine" not in vendor_map:
                vendor_map["wine"] = vendor
            if ("beer" in notes or "local beer" in notes) and "beer" not in vendor_map:
                vendor_map["beer"] = vendor
            if ("craft" in notes and ("can" in notes or "bottle" in notes)) and "craft_beer" not in vendor_map:
                vendor_map["craft_beer"] = vendor

    return vendor_map


def _resolve_vendor(category: str, vendor_map: dict[str, str]) -> str:
    """Resolve a category to a vendor name."""
    if category in vendor_map:
        return vendor_map[category]
    # Fallback: return unknown
    return "Unknown Vendor"


def run(ctx: object) -> Result:
    """Parse inventory-check output and generate order recommendations by vendor."""
    log.event("vendor_order_review.started")

    input_file = getattr(ctx.args, "input_file", None)
    if not input_file:
        log.event("vendor_order_review.error", reason="no_input_file")
        return {
            "skill": "vendor-order-review",
            "status": "fail",
            "summary": "No --input-file provided.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    input_path = Path(input_file)

    # Determine allowlist root for input file
    allowlist_root = input_path.parent

    resolved_input = io.read_allowed_path(input_path, allowlist_root=allowlist_root)
    if resolved_input is None:
        log.event("vendor_order_review.error", reason="input_file_missing")
        return {
            "skill": "vendor-order-review",
            "status": "fail",
            "summary": "Input file not found: {path}.".format(path=input_file),
            "data": {},
            "findings": [],
            "metrics": {},
        }

    input_text = resolved_input.read_text(encoding="utf-8")
    try:
        input_data = json.loads(input_text)
    except (json.JSONDecodeError, ValueError):
        log.event("vendor_order_review.error", reason="invalid_json")
        return {
            "skill": "vendor-order-review",
            "status": "fail",
            "summary": "Input file is not valid JSON.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    low_stock = input_data.get("data", {}).get("low_stock", [])

    # Load vendor map from docs
    inventory_dir = ctx.args.inventory_dir or (MAYA_ROOT / "docs" / "inventory")
    inventory_dir = Path(inventory_dir)

    # Vendor docs: look for vendors.md in fixture dir or docs/vendors/README.md
    if ctx.args.inventory_dir:
        vendors_path = inventory_dir / "vendors.md"
        vendors_root = inventory_dir
    else:
        vendors_path = MAYA_ROOT / "docs" / "vendors" / "README.md"
        vendors_root = MAYA_ROOT / "docs"

    vendor_map = _load_vendor_map(vendors_path, allowlist_root=vendors_root)

    if not low_stock:
        log.event("vendor_order_review.finished", orders_count=0)
        return {
            "skill": "vendor-order-review",
            "status": "ok",
            "summary": "No low stock items. No orders needed.",
            "data": {"orders_by_vendor": {}, "total_items": 0},
            "findings": [],
            "metrics": {},
        }

    # Group by vendor and calculate order quantities
    orders_by_vendor: dict[str, list[dict]] = {}
    for item in low_stock:
        category = item.get("category", "unknown")
        vendor = _resolve_vendor(category, vendor_map)
        par = item.get("par")
        qty = item.get("qty", 0)

        if par is not None:
            order_qty = par - qty
        else:
            # Fallback: order enough to reach reorder_at + small buffer
            reorder_at = item.get("reorder_at", 0)
            order_qty = reorder_at - qty + 1

        if order_qty <= 0:
            order_qty = 1

        order_entry = {
            "item": item.get("item", "unknown"),
            "category": category,
            "current_qty": qty,
            "par": par,
            "order_qty": order_qty,
        }

        if vendor not in orders_by_vendor:
            orders_by_vendor[vendor] = []
        orders_by_vendor[vendor].append(order_entry)

    # Build findings
    findings = []
    total_items = 0
    for vendor, orders in orders_by_vendor.items():
        for order in orders:
            total_items += 1
            findings.append({
                "severity": "warn",
                "code": "ORDER_NEEDED",
                "subject": "{vendor}/{item}".format(vendor=vendor, item=order["item"]),
                "message": "Order {qty} x {item} from {vendor} (current: {current}, par: {par}).".format(
                    qty=order["order_qty"],
                    item=order["item"],
                    vendor=vendor,
                    current=order["current_qty"],
                    par=order["par"],
                ),
            })

    status = "warn"
    summary = "{count} item(s) need ordering from {vendors} vendor(s).".format(
        count=total_items,
        vendors=len(orders_by_vendor),
    )

    log.event(
        "vendor_order_review.finished",
        orders_count=total_items,
        vendor_count=len(orders_by_vendor),
    )

    return {
        "skill": "vendor-order-review",
        "status": status,
        "summary": summary,
        "data": {"orders_by_vendor": orders_by_vendor, "total_items": total_items},
        "findings": findings,
        "metrics": {},
    }
