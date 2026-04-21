---
name: schedule-draft
description: Generate a draft weekly schedule with labor law checks.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [schedule, staff, draft, labor-law]
    requires_toolsets: [terminal]
    config:
      - key: schedule_dir
        description: "Path to schedule docs directory"
        default: "docs/schedule"
required_environment_variables: []
---

# Schedule Draft

Generate a draft weekly schedule based on staff availability, max hours, and certifications. Flags labor law concerns including CA overtime rules, SF predictive scheduling ordinance, and missing RBS certifications.

## When to Use

- When creating next week's schedule
- When checking labor law compliance for a proposed schedule
- Before publishing a new schedule

## Procedure

```bash
python -m skills.schedule_draft --format json
python -m skills.schedule_draft --format json --week-of 2026-04-20
python -m skills.schedule_draft --format json --schedule-dir docs/schedule
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK, no labor law findings |
| 1 | Warnings present (overtime risk, missing cert, etc.) |
| 2 | Config error |
| 3 | Data error (missing staff.md) |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.shifts` contains generated schedule entries
- `findings` lists any labor law concerns with codes: OVERTIME_RISK, PREDICTIVE_SCHED, MISSING_CERT
