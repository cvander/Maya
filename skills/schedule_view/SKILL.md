---
name: schedule-view
description: Display the current weekly staff schedule.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [schedule, staff, view]
    requires_toolsets: [terminal]
    config:
      - key: schedule_dir
        description: "Path to schedule docs directory"
        default: "docs/schedule"
required_environment_variables: []
---

# Schedule View

Display the current weekly staff schedule with shift details and hours summary.

## When to Use

- When Maya or staff need to see the current week's schedule
- When checking total hours per staff member
- Before making scheduling decisions

## Procedure

```bash
python -m skills.schedule_view --format json
python -m skills.schedule_view --format json --week-of 2026-04-13
python -m skills.schedule_view --format json --schedule-dir docs/schedule
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK |
| 1 | Warnings/findings present |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.entries` contains parsed schedule rows
- `data.staff_hours` contains per-staff hour totals
