---
name: music-calendar
description: View and filter the music booking calendar.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [music, calendar, entertainment, bar-ops]
    requires_toolsets: [terminal]
    config:
      - key: music.dir
        description: "Path to music data directory"
        default: "docs/music"
required_environment_variables: []
---

# Music Calendar

View and filter upcoming music events from the booking calendar.

## When to Use

- When Maya needs to check upcoming music events
- When filtering events by date range or status
- When calculating total booking fees for a period

## Procedure

```bash
python -m skills.music_calendar --from 2026-04-01 --to 2026-04-30 --status confirmed --format json
```

### Arguments

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--from YYYY-MM-DD` | no | today | Start date |
| `--to YYYY-MM-DD` | no | from + weeks | End date |
| `--weeks N` | no | 4 | Weeks to look ahead |
| `--status all\|confirmed\|tentative\|pending` | no | all | Filter by status |
| `--music-dir PATH` | no | docs/music | Override music data directory |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK - calendar retrieved |
| 1 | Warnings present |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0
- stdout is valid JSON (with --format json)
- `data.events` is a list of event objects
- `data.total_fees` is an integer
