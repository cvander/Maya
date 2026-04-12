"""vendor-contact -- Generate email body or phone script for a vendor."""

from __future__ import annotations

from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.md_table import parse_tables
from skills._lib.result import Result


def _find_vendor(tables: list[list[dict[str, str]]], vendor_name: str) -> dict[str, str] | None:
    """Find a vendor row by name (case-insensitive) across all tables."""
    for table in tables:
        for row in table:
            # Check both "vendor" and "contact" column names
            name = row.get("vendor", "").strip()
            if not name:
                # Direct/Walk-In table might not have "vendor" column
                # Try matching on the first non-empty value
                for key in ("vendor", "contact"):
                    val = row.get(key, "").strip()
                    if val:
                        name = val
                        break
            if name.lower() == vendor_name.lower():
                return row
    return None


def _build_email(vendor_name: str, vendor_row: dict[str, str]) -> str:
    """Build an email body for a vendor order."""
    rep = vendor_row.get("rep", "").strip()
    email = vendor_row.get("email", "").strip()

    lines = []
    if rep:
        lines.append("Hi {rep},".format(rep=rep))
    else:
        lines.append("Hi,")
    lines.append("")
    lines.append("I'd like to place an order for Maya. Details below:")
    lines.append("")
    lines.append("[INSERT ORDER DETAILS HERE]")
    lines.append("")
    lines.append("Please confirm availability and delivery date.")
    lines.append("")
    lines.append("Thanks,")
    lines.append("Maya")

    return "\n".join(lines)


def _build_phone_script(vendor_name: str, vendor_row: dict[str, str]) -> str:
    """Build a phone script for a vendor order."""
    rep = vendor_row.get("rep", "").strip()
    phone = vendor_row.get("phone", "").strip()
    account = vendor_row.get("account #", "").strip()

    lines = []
    if rep:
        lines.append("Ask for: {rep}".format(rep=rep))
    else:
        lines.append("Ask for: the sales rep for Maya")
    if account:
        lines.append("Account: {account}".format(account=account))
    lines.append("")
    lines.append("Script:")
    lines.append("Hi, this is Maya calling to place an order.")
    if account:
        lines.append("Account number: {account}.".format(account=account))
    lines.append("[READ ORDER DETAILS]")
    lines.append("What's the earliest delivery date?")
    lines.append("Thanks.")

    return "\n".join(lines)


def run(ctx: object) -> Result:
    """Generate contact draft for a vendor."""
    log.event("vendor_contact.started")

    vendor = getattr(ctx.args, "vendor", None)
    method = getattr(ctx.args, "method", None)

    if not vendor:
        log.event("vendor_contact.error", reason="no_vendor")
        return {
            "skill": "vendor-contact",
            "status": "fail",
            "summary": "No --vendor provided.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    if not method:
        log.event("vendor_contact.error", reason="no_method")
        return {
            "skill": "vendor-contact",
            "status": "fail",
            "summary": "No --method provided. Use --method email or --method phone.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    # Load vendor docs
    inventory_dir = ctx.args.inventory_dir
    if inventory_dir:
        vendors_path = Path(inventory_dir) / "vendors.md"
        vendors_root = Path(inventory_dir)
    else:
        vendors_path = MAYA_ROOT / "docs" / "vendors" / "README.md"
        vendors_root = MAYA_ROOT / "docs"

    resolved = io.read_allowed_path(vendors_path, allowlist_root=vendors_root)
    if resolved is None:
        log.event("vendor_contact.error", reason="vendors_file_missing")
        return {
            "skill": "vendor-contact",
            "status": "fail",
            "summary": "Vendor docs not found.",
            "data": {},
            "findings": [],
            "metrics": {},
        }

    text = resolved.read_text(encoding="utf-8")
    tables = parse_tables(text)

    vendor_row = _find_vendor(tables, vendor)
    if vendor_row is None:
        log.event("vendor_contact.finished", vendor=vendor, found=False)
        return {
            "skill": "vendor-contact",
            "status": "ok",
            "summary": "Vendor not found: {vendor}.".format(vendor=vendor),
            "data": {"vendor": vendor, "message": "", "contact_info": {}},
            "findings": [],
            "metrics": {},
        }

    # Extract contact info
    contact_info = {
        "vendor": vendor_row.get("vendor", "").strip() or vendor,
        "rep": vendor_row.get("rep", "").strip(),
        "phone": vendor_row.get("phone", "").strip(),
        "email": vendor_row.get("email", "").strip(),
    }

    if method == "email":
        message = _build_email(vendor, vendor_row)
    else:
        message = _build_phone_script(vendor, vendor_row)

    findings = [
        {
            "severity": "info",
            "code": "CONTACT_DRAFT",
            "subject": vendor,
            "message": "{method} draft generated for {vendor}.".format(
                method=method.capitalize(),
                vendor=vendor,
            ),
        }
    ]

    log.event(
        "vendor_contact.finished",
        vendor=vendor,
        method=method,
        found=True,
    )

    return {
        "skill": "vendor-contact",
        "status": "warn",
        "summary": "{method} draft for {vendor}.".format(
            method=method.capitalize(),
            vendor=vendor,
        ),
        "data": {
            "vendor": vendor,
            "method": method,
            "message": message,
            "contact_info": contact_info,
        },
        "findings": findings,
        "metrics": {},
    }
