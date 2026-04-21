"""compliance-check -- scan compliance docs for expiring certs, overdue logs, and permit renewals."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log, md_table
from skills._lib.result import Result


def _parse_date(value: str | None) -> date | None:
    """Parse a YYYY-MM-DD date string, return None on failure."""
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return date.fromisoformat(stripped)
    except (ValueError, TypeError):
        return None


def _check_staff_certs(
    compliance_dir: Path, allowlist_root: Path, ref_date: date, days_ahead: int
) -> tuple[list[dict], int]:
    """Check staff certifications for expiring/expired certs."""
    findings = []
    certs_checked = 0

    fpath = compliance_dir / "staff-certs.md"
    resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("compliance_check.file_missing", file="staff-certs.md")
        return findings, certs_checked

    text = resolved.read_text(encoding="utf-8")
    for table in md_table.parse_tables(text):
        for row in table:
            name = row.get("name", "").strip()
            expires_str = row.get("expires", "").strip()
            if not name or not expires_str:
                continue

            expires = _parse_date(expires_str)
            if expires is None:
                continue

            certs_checked += 1
            days_until = (expires - ref_date).days

            if days_until < 0:
                findings.append({
                    "severity": "fail",
                    "code": "CERT_EXPIRED",
                    "subject": name,
                    "message": "{name}: RBS cert expired on {expires} ({days} days ago).".format(
                        name=name, expires=expires_str, days=abs(days_until)
                    ),
                })
            elif days_until <= days_ahead:
                findings.append({
                    "severity": "warn",
                    "code": "CERT_EXPIRING",
                    "subject": name,
                    "message": "{name}: RBS cert expires on {expires} ({days} days).".format(
                        name=name, expires=expires_str, days=days_until
                    ),
                })

    log.event("compliance_check.certs_checked", count=certs_checked)
    return findings, certs_checked


def _find_latest_date_in_table(text: str) -> date | None:
    """Find the most recent date value in any table in the text."""
    latest = None
    for table in md_table.parse_tables(text):
        for row in table:
            date_val = _parse_date(row.get("date", ""))
            if date_val is not None:
                if latest is None or date_val > latest:
                    latest = date_val
    return latest


def _check_cooler_temps(
    compliance_dir: Path, allowlist_root: Path, ref_date: date
) -> tuple[list[dict], bool]:
    """Check cooler temperature log for overdue entries."""
    findings = []
    checked = False
    max_gap_days = 7

    fpath = compliance_dir / "cooler-temps.md"
    resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("compliance_check.file_missing", file="cooler-temps.md")
        return findings, checked

    text = resolved.read_text(encoding="utf-8")
    checked = True
    latest = _find_latest_date_in_table(text)

    if latest is None:
        findings.append({
            "severity": "warn",
            "code": "LOG_OVERDUE",
            "subject": "cooler-temps",
            "message": "Cooler temperature log has no dated entries.",
        })
    else:
        gap = (ref_date - latest).days
        if gap > max_gap_days:
            findings.append({
                "severity": "warn",
                "code": "LOG_OVERDUE",
                "subject": "cooler-temps",
                "message": "Cooler temperature log last updated {last} ({gap} days ago, max {max} days).".format(
                    last=latest.isoformat(), gap=gap, max=max_gap_days
                ),
            })

    log.event("compliance_check.cooler_checked", latest_date=str(latest))
    return findings, checked


def _check_pest_log(
    compliance_dir: Path, allowlist_root: Path, ref_date: date
) -> tuple[list[dict], bool]:
    """Check pest control log for overdue inspections."""
    findings = []
    checked = False
    max_gap_days = 30

    fpath = compliance_dir / "pest-log.md"
    resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("compliance_check.file_missing", file="pest-log.md")
        return findings, checked

    text = resolved.read_text(encoding="utf-8")
    checked = True
    latest = _find_latest_date_in_table(text)

    if latest is None:
        findings.append({
            "severity": "warn",
            "code": "LOG_OVERDUE",
            "subject": "pest-log",
            "message": "Pest control log has no dated entries.",
        })
    else:
        gap = (ref_date - latest).days
        if gap > max_gap_days:
            findings.append({
                "severity": "warn",
                "code": "LOG_OVERDUE",
                "subject": "pest-log",
                "message": "Pest control log last updated {last} ({gap} days ago, max {max} days).".format(
                    last=latest.isoformat(), gap=gap, max=max_gap_days
                ),
            })

    log.event("compliance_check.pest_checked", latest_date=str(latest))
    return findings, checked


def _check_permits(
    compliance_dir: Path, allowlist_root: Path, ref_date: date, days_ahead: int
) -> tuple[list[dict], int]:
    """Check permits/README.md for upcoming renewals and inspections."""
    findings = []
    permits_checked = 0

    # permits dir is sibling to compliance dir
    permits_dir = compliance_dir.parent / "permits"
    fpath = permits_dir / "README.md"
    resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)
    if resolved is None:
        log.event("compliance_check.file_missing", file="permits/README.md")
        return findings, permits_checked

    text = resolved.read_text(encoding="utf-8")

    # Check renewal calendar table
    for table in md_table.parse_tables(text):
        for row in table:
            permit = row.get("permit", "").strip()
            renewal_str = row.get("renewal date", "").strip()
            if not permit:
                continue

            renewal_date = _parse_date(renewal_str)
            if renewal_date is None:
                continue

            permits_checked += 1
            days_until = (renewal_date - ref_date).days

            if days_until <= days_ahead and days_until >= 0:
                findings.append({
                    "severity": "warn",
                    "code": "PERMIT_RENEWAL",
                    "subject": permit,
                    "message": "{permit}: renewal due {date} ({days} days).".format(
                        permit=permit, date=renewal_str, days=days_until
                    ),
                })

    # Check inspections table for "Next Expected" column
    for table in md_table.parse_tables(text):
        for row in table:
            itype = row.get("type", "").strip()
            next_str = row.get("next expected", "").strip()
            if not itype or not next_str:
                continue

            next_date = _parse_date(next_str)
            if next_date is None:
                continue

            days_until = (next_date - ref_date).days
            if days_until <= days_ahead and days_until >= 0:
                findings.append({
                    "severity": "warn",
                    "code": "INSPECTION_DUE",
                    "subject": itype,
                    "message": "{type} inspection expected {date} ({days} days).".format(
                        type=itype, date=next_str, days=days_until
                    ),
                })

    log.event("compliance_check.permits_checked", count=permits_checked)
    return findings, permits_checked


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("compliance_check.started")

    ref_date_str = getattr(ctx.args, "date", None)
    if ref_date_str:
        ref_date = _parse_date(ref_date_str)
        if ref_date is None:
            return {
                "skill": "compliance-check",
                "status": "fail",
                "summary": "Invalid --date: {val}".format(val=ref_date_str),
                "data": {},
                "findings": [],
                "metrics": {},
            }
    else:
        ref_date = date.today()

    days_ahead = getattr(ctx.args, "days_ahead", 30)
    compliance_dir_arg = getattr(ctx.args, "compliance_dir", None)

    if compliance_dir_arg:
        compliance_dir = Path(compliance_dir_arg)
        allowlist_root = compliance_dir.parent
    else:
        compliance_dir = MAYA_ROOT / "docs" / "compliance"
        allowlist_root = MAYA_ROOT / "docs"

    findings = []

    # Check staff certifications
    cert_findings, certs_checked = _check_staff_certs(
        compliance_dir, allowlist_root, ref_date, days_ahead
    )
    findings.extend(cert_findings)

    # Check cooler temperature log
    cooler_findings, cooler_checked = _check_cooler_temps(
        compliance_dir, allowlist_root, ref_date
    )
    findings.extend(cooler_findings)

    # Check pest control log
    pest_findings, pest_checked = _check_pest_log(
        compliance_dir, allowlist_root, ref_date
    )
    findings.extend(pest_findings)

    # Check permits
    permit_findings, permits_checked = _check_permits(
        compliance_dir, allowlist_root, ref_date, days_ahead
    )
    findings.extend(permit_findings)

    logs_checked = sum([1 for c in [cooler_checked, pest_checked] if c])

    status = "warn" if findings else "ok"
    if findings:
        summary = "{count} compliance finding(s) as of {date}.".format(
            count=len(findings), date=ref_date.isoformat()
        )
    else:
        summary = "All compliance items current as of {date}.".format(
            date=ref_date.isoformat()
        )

    log.event(
        "compliance_check.finished",
        status=status,
        findings_count=len(findings),
    )

    return {
        "skill": "compliance-check",
        "status": status,
        "summary": summary,
        "data": {
            "ref_date": ref_date.isoformat(),
            "days_ahead": days_ahead,
            "certs_checked": certs_checked,
            "logs_checked": logs_checked,
            "permits_checked": permits_checked,
        },
        "findings": findings,
        "metrics": {},
    }
