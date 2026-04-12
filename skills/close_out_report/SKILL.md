---
name: close-out-report
description: "Aggregate close-out data over a date range."
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [close-out, report, analytics, revenue]
    requires_toolsets: [terminal]
    config: []
required_environment_variables: []
---

# Close-Out Report

Reads close-out reconciliation files from data/close-out/ and aggregates them into a summary report. Shows total revenue, average variance, tip trends, and waste frequency over a date range.

## When to Use

- Weekly or monthly review of bar performance
- When Maya needs to spot cash variance trends
- When waste patterns need analysis

## Procedure

```bash
python -m skills.close_out_report --format json --from 2026-04-01 --to 2026-04-10
```

Optional: `--data-dir PATH` (defaults to data/close-out).

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK |
| 1 | Warnings present |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0
- stdout is valid JSON (with --format json)
- `data` field contains aggregated revenue, variance, and waste stats
