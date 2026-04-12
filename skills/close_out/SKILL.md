---
name: close-out
description: "Nightly cash reconciliation, tip split, and waste logging."
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [close-out, cash, tips, waste, nightly]
    requires_toolsets: [terminal]
    config: []
required_environment_variables: []
---

# Close-Out

Nightly cash reconciliation, tip split, and waste logging. Calculates variance between actual and expected revenue, splits tips 80/20 staff/house, and logs waste items. Writes a reconciliation report to data/close-out/.

## When to Use

- At end of each shift or night to reconcile the register
- When Maya needs to log waste from the bar
- When tip splits need to be calculated and recorded

## Procedure

```bash
python -m skills.close_out --format json \
  --cash-count 850.00 \
  --card-total 1200.00 \
  --expected 2045.00 \
  --tip-total 320.00 \
  --waste-items "lime:5,beer:2"
```

Optional: `--date YYYY-MM-DD` (defaults to today), `--data-dir PATH` (defaults to data/close-out).

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK, variance within threshold |
| 1 | Warnings: cash over/short beyond $5 threshold |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data` field contains variance, tip split, and waste items
- Reconciliation file written to data/close-out/YYYY-MM-DD.md
