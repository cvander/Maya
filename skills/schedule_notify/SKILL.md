---
name: schedule-notify
description: Generate per-staff notification messages from a schedule.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [schedule, staff, notify, messages]
    requires_toolsets: [terminal]
    config: []
required_environment_variables: []
---

# Schedule Notify

Parse schedule JSON output (from schedule-view or schedule-draft) and generate per-staff notification messages ready to copy-paste.

## When to Use

- After generating a schedule with schedule-view or schedule-draft
- When staff need to be notified of their upcoming shifts
- Before publishing a finalized schedule

## Procedure

```bash
python -m skills.schedule_view --format json > /tmp/schedule.json
python -m skills.schedule_notify --format json --input-file /tmp/schedule.json
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK, notifications generated |
| 1 | Warnings (no shifts found) |
| 2 | Config error |
| 3 | Data error (missing or invalid input file) |
| 10 | Unexpected error |

## Verification

- Exit code is 0
- stdout is valid JSON (with --format json)
- `data.notifications` contains one entry per staff member
- Each notification has `staff`, `shift_count`, `total_hours`, and `message` fields
