"""Structured JSONL logging for Maya skills."""

import json
from datetime import datetime, timezone
from pathlib import Path

from . import MAYA_ROOT

_LOG_DIR = MAYA_ROOT / "logs" / "skills"


def event(name: str, **fields: object) -> None:
    """Append a structured log event to logs/skills/<skill>.jsonl.

    The log file is derived from the first dotted segment of the event name.
    Fields must be JSON-serializable primitives. No f-strings, no free-text.
    """
    skill_prefix = name.split(".")[0]
    log_file = _LOG_DIR / "{prefix}.jsonl".format(prefix=skill_prefix)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "event": name,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    entry.update(fields)
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
