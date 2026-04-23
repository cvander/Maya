# Skill Contract

Every Maya skill follows this contract. Read it once, refer back as needed.

## Inputs

A skill is invoked as `python -m skills.<name>`. Shared CLI flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--format {text,json}` | `text` | Output format |
| `--verbose` | off | Extra log output |
| `--inventory-dir PATH` | `docs/inventory` | Override inventory root |

## Outputs

A skill returns a single **Result** dict, emitted via `_lib.io.emit()`:

```json
{
  "skill": "skill-name",
  "status": "ok | warn | fail",
  "summary": "One-line human summary.",
  "data": {},
  "findings": [
    {"severity": "info|warn|fail", "code": "CODE", "subject": "what", "message": "details."}
  ],
  "metrics": {"duration_ms": 0}
}
```

Skills never call `print()` directly. All output goes through `_lib.io.emit()`.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK, no findings requiring action |
| 1 | Warn, findings present (e.g. low stock) |
| 2 | Config error (bad args, missing manifest) |
| 3 | Data error (can't read source files) |
| 4 | External dependency error (reserved) |
| 5 | Safety refusal (reserved for Phase 3) |
| 10 | Unexpected exception |

## Manifest

Each skill has a `manifest.toml` declaring its properties:

```toml
[skill]
name = "skill-name"
version = "0.1.0"
description = "What this skill does."
safety = "read_only"         # read_only | idempotent | mutating_non_idempotent
pii_scope = "none"           # none | inventory | guest | staff
failure_mode = "advisory"    # advisory | guarding
reads = ["docs/inventory/*.md"]
writes = []
network = false
hard_stops_touched = []
env_required = []
```

## SKILL.md (Orchestrator Discovery)

Each skill MAY include a `SKILL.md` for Hermes orchestrator discovery. This is separate from `manifest.toml`:

- **manifest.toml** = runtime safety declarations (consumed by runner.py, Phase 3 enforcer)
- **SKILL.md** = orchestrator discovery and invocation guide (consumed by Hermes agent)

A skill can exist without SKILL.md (CLI-only use), but any skill intended for Hermes scheduling must have one.

### Format

YAML frontmatter followed by markdown:

```yaml
---
name: skill-name          # must match manifest.toml [skill].name
description: Brief desc    # must match manifest.toml [skill].description
version: 0.1.0            # must match manifest.toml [skill].version
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [keywords]
    requires_tools: [terminal]
    config:
      - key: config.key
        description: "desc"
        default: "value"
required_environment_variables: []  # must match manifest.toml env_required
---
```

### Required Sections

| Section | Purpose |
|---------|---------|
| When to Use | Conditions that should trigger this skill |
| Procedure | Exact CLI command and how to interpret output |
| Verification | How to confirm the skill ran successfully |

### Rules

- `name`, `version`, `description` must match `manifest.toml`. Don't drift.
- `required_environment_variables` must match `env_required` in manifest.toml.
- Procedure must include the exact CLI command.
- Verification must reference exit codes from this contract.

## Logging

Skills log via `_lib.log.event(name, **fields)`. Events are appended as JSONL to `logs/skills/<skill>.jsonl`.

Rules:

- Event names are fixed dotted strings (e.g. `inventory_check.started`). No f-strings in names.
- Fields are structured scalars only: counts, file names, exit codes, durations.
- No free-text interpolation. No item names, brand names, or PII in log fields.

## File Reads

Skills read files via `_lib.io.read_allowed_path(path, allowlist_root)`.

- Returns file content path if the file exists, `None` if missing.
- Raises `PermissionError` if the resolved path escapes the allowlist root.
- Resolves symlinks and checks `is_relative_to`.
- Skills never call `open()` directly.

## Testing

- stdlib `unittest` only. No pytest, no third-party test libs.
- Golden-output pattern: run skill against fixtures, diff Result JSON against `expected.json`.
- Fixtures use fictional data only (see `FIXTURES.md` in each skill).
- `fixtures/local/` is gitignored for real data testing.

## Safety Declaration

The manifest's `safety`, `pii_scope`, `reads`, `writes`, `network`, `hard_stops_touched`, and `env_required` fields declare the skill's boundaries. Phase 3 will enforce these declarations at runtime.
