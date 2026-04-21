"""vendor-order -- Generate copy-paste-ready order text for a specific vendor."""

from __future__ import annotations

import json
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.result import Result


def run(ctx: object) -> Result:
    """Filter vendor-order-review output for a vendor and format as order text."""
    log.event("vendor_order.started")

    vendor = getattr(ctx.args, "vendor", None)
    input_file = getattr(ctx.args, "input_file", None)

    if not vendor:
        log.event("vendor_order.error", reason="no_vendor")
        return {
            "skill": "vendor-order",
            "status": "fail",
            "summary": "No --vendor provided.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    if not input_file:
        log.event("vendor_order.error", reason="no_input_file")
        return {
            "skill": "vendor-order",
            "status": "fail",
            "summary": "No --input-file provided.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    input_path = Path(input_file)
    allowlist_root = input_path.parent

    resolved_input = io.read_allowed_path(input_path, allowlist_root=allowlist_root)
    if resolved_input is None:
        log.event("vendor_order.error", reason="input_file_missing")
        return {
            "skill": "vendor-order",
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
        log.event("vendor_order.error", reason="invalid_json")
        return {
            "skill": "vendor-order",
            "status": "fail",
            "summary": "Input file is not valid JSON.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    orders_by_vendor = input_data.get("data", {}).get("orders_by_vendor", {})

    # Find the vendor (case-insensitive match)
    matched_vendor = None
    matched_orders = None
    for v, orders in orders_by_vendor.items():
        if v.lower() == vendor.lower():
            matched_vendor = v
            matched_orders = orders
            break

    if matched_vendor is None or not matched_orders:
        log.event("vendor_order.finished", vendor=vendor, items_count=0)
        return {
            "skill": "vendor-order",
            "status": "ok",
            "summary": "No orders found for vendor: {vendor}.".format(vendor=vendor),
            "data": {"vendor": vendor, "order_text": "", "items_count": 0},
            "findings": [],
            "metrics": {},
        }

    # Build plain text order (copy-paste ready, not markdown)
    lines = []
    lines.append("ORDER FOR: {vendor}".format(vendor=matched_vendor))
    lines.append("")
    for i, order in enumerate(matched_orders, 1):
        lines.append("{n}. {item} - Qty: {qty}".format(
            n=i,
            item=order["item"],
            qty=order["order_qty"],
        ))
    lines.append("")
    lines.append("Total items: {count}".format(count=len(matched_orders)))

    order_text = "\n".join(lines)

    findings = [
        {
            "severity": "info",
            "code": "ORDER_DRAFT",
            "subject": matched_vendor,
            "message": "Draft order for {vendor} with {count} item(s).".format(
                vendor=matched_vendor,
                count=len(matched_orders),
            ),
        }
    ]

    log.event(
        "vendor_order.finished",
        vendor=matched_vendor,
        items_count=len(matched_orders),
    )

    return {
        "skill": "vendor-order",
        "status": "warn",
        "summary": "Order draft for {vendor}: {count} item(s).".format(
            vendor=matched_vendor,
            count=len(matched_orders),
        ),
        "data": {
            "vendor": matched_vendor,
            "order_text": order_text,
            "items_count": len(matched_orders),
        },
        "findings": findings,
        "metrics": {},
    }
