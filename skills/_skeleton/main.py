"""<Skill Name> -- <one-line description>."""

from __future__ import annotations

from skills._lib import MAYA_ROOT, io, log
from skills._lib.result import Result


def run(ctx: object) -> Result:
    """Main skill entry point."""
    log.event("<skill_name>.started")

    findings = []
    data = {}

    # TODO: implement skill logic
    # Use io.read_allowed_path() for file reads
    # Use io.write_allowed_path() / io.atomic_write_text() for file writes
    # Use log.event() for structured logging
    # Build findings list with severity/code/subject/message

    status = "warn" if findings else "ok"
    summary = "{count} finding(s).".format(count=len(findings)) if findings else "All clear."

    log.event("<skill_name>.finished", status=status, findings_count=len(findings))

    return {
        "skill": "<skill-name>",
        "status": status,
        "summary": summary,
        "data": data,
        "findings": findings,
        "metrics": {},
    }
