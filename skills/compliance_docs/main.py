"""compliance-docs -- audit compliance documentation for completeness and freshness."""

from __future__ import annotations

import os
from datetime import date, timedelta
from pathlib import Path

from skills._lib import MAYA_ROOT, io, log
from skills._lib.result import Result


# Expected compliance docs (relative to compliance_dir)
_EXPECTED_COMPLIANCE_DOCS = [
    "staff-certs.md",
    "cooler-temps.md",
    "pest-log.md",
    "incidents.md",
]

# Expected permit docs (relative to compliance_dir parent / permits)
_EXPECTED_PERMIT_DOCS = [
    "permits/README.md",
]

_STALE_THRESHOLD_DAYS = 30
_MIN_CONTENT_LENGTH = 20  # bytes, to distinguish empty from meaningful


def _check_doc(
    fpath: Path, allowlist_root: Path, label: str
) -> tuple[dict | None, dict]:
    """Check a single doc. Returns (finding_or_None, info_dict)."""
    resolved = io.read_allowed_path(fpath, allowlist_root=allowlist_root)

    if resolved is None:
        finding = {
            "severity": "warn",
            "code": "DOC_MISSING",
            "subject": label,
            "message": "{label}: expected compliance doc not found.".format(label=label),
        }
        info = {"name": label, "status": "missing", "last_modified": None}
        return finding, info

    # Check if empty
    text = resolved.read_text(encoding="utf-8").strip()
    # Strip markdown headers and whitespace to check for meaningful content
    lines = [
        ln for ln in text.splitlines()
        if ln.strip() and not ln.strip().startswith("#") and ln.strip() != "---"
    ]
    # Filter out lines that are only table headers/separators with no data
    content_lines = []
    for ln in lines:
        stripped = ln.strip()
        # Skip pure separator rows like |---|---|
        if stripped.startswith("|") and all(
            c in "-| " for c in stripped
        ):
            continue
        content_lines.append(stripped)

    if len(content_lines) == 0:
        finding = {
            "severity": "warn",
            "code": "DOC_EMPTY",
            "subject": label,
            "message": "{label}: doc exists but has no meaningful entries.".format(label=label),
        }
        info = {"name": label, "status": "empty", "last_modified": _get_mtime_iso(resolved)}
        return finding, info

    # Check staleness via file mtime
    mtime_date = _get_mtime_date(resolved)
    today = date.today()
    if mtime_date and (today - mtime_date).days > _STALE_THRESHOLD_DAYS:
        finding = {
            "severity": "info",
            "code": "DOC_STALE",
            "subject": label,
            "message": "{label}: not updated in {days} days (last modified {mtime}).".format(
                label=label,
                days=(today - mtime_date).days,
                mtime=mtime_date.isoformat(),
            ),
        }
        info = {"name": label, "status": "stale", "last_modified": mtime_date.isoformat()}
        return finding, info

    info = {
        "name": label,
        "status": "ok",
        "last_modified": _get_mtime_iso(resolved),
    }
    return None, info


def _get_mtime_date(path: Path) -> date | None:
    """Get file modification time as a date."""
    try:
        stat = path.stat()
        return date.fromtimestamp(stat.st_mtime)
    except OSError:
        return None


def _get_mtime_iso(path: Path) -> str | None:
    """Get file modification time as ISO date string."""
    d = _get_mtime_date(path)
    return d.isoformat() if d else None


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("compliance_docs.started")

    compliance_dir_arg = getattr(ctx.args, "compliance_dir", None)

    if compliance_dir_arg:
        compliance_dir = Path(compliance_dir_arg)
        allowlist_root = compliance_dir.parent
    else:
        compliance_dir = MAYA_ROOT / "docs" / "compliance"
        allowlist_root = MAYA_ROOT / "docs"

    findings = []
    doc_infos = []
    docs_present = 0
    docs_missing = 0

    # Check compliance docs
    for fname in _EXPECTED_COMPLIANCE_DOCS:
        fpath = compliance_dir / fname
        label = fname
        finding, info = _check_doc(fpath, allowlist_root, label)
        doc_infos.append(info)
        if info["status"] == "missing":
            docs_missing += 1
        else:
            docs_present += 1
        if finding:
            findings.append(finding)
        log.event("compliance_docs.doc_checked", file=fname, status=info["status"])

    # Check permit docs
    for fname in _EXPECTED_PERMIT_DOCS:
        fpath = compliance_dir.parent / fname
        label = fname
        finding, info = _check_doc(fpath, allowlist_root, label)
        doc_infos.append(info)
        if info["status"] == "missing":
            docs_missing += 1
        else:
            docs_present += 1
        if finding:
            findings.append(finding)
        log.event("compliance_docs.doc_checked", file=fname, status=info["status"])

    docs_checked = docs_present + docs_missing
    status = "warn" if findings else "ok"

    if findings:
        summary = "{count} documentation issue(s) found across {total} expected docs.".format(
            count=len(findings), total=docs_checked
        )
    else:
        summary = "All {total} expected compliance docs present and current.".format(
            total=docs_checked
        )

    log.event(
        "compliance_docs.finished",
        status=status,
        findings_count=len(findings),
    )

    return {
        "skill": "compliance-docs",
        "status": status,
        "summary": summary,
        "data": {
            "docs_checked": docs_checked,
            "docs_present": docs_present,
            "docs_missing": docs_missing,
            "docs": doc_infos,
        },
        "findings": findings,
        "metrics": {},
    }
