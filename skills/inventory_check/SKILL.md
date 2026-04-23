---
name: inventory-check
description: Scan inventory markdown for items at or below reorder threshold.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [inventory, stock, reorder, bar-ops]
    requires_tools: [terminal]
    config:
      - key: inventory_dir
        description: "Path to inventory markdown files"
        default: "docs/inventory"
required_environment_variables: []
---

# Inventory Check

Reads beer.md, spirits.md, and wine.md from the inventory directory. Compares each item's quantity against its reorder threshold. Reports items at or below threshold.

Read-only. Does not modify files or reach external services. No PII in output.

## When to Use

- Daily morning check before opening (scheduled: 10:00 AM)
- Before placing vendor orders (Sunday/Monday)
- When a bartender reports running low on something
- After receiving a delivery, to confirm stock levels updated

## Procedure

Run the skill from the repo root:

```bash
# Human-readable summary
python -m skills.inventory_check

# Structured JSON output (for automation)
python -m skills.inventory_check --format json

# Against a custom inventory directory
python -m skills.inventory_check --inventory-dir path/to/inventory --format json
```

Parse the JSON result:

- `status`: "ok" (nothing to reorder) or "warn" (items need attention)
- `findings`: array of LOW_STOCK items with category, item name, qty, reorder_at
- `data.items_scanned`: total items checked
- `data.low_stock`: detailed list of low items

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All stock levels acceptable |
| 1 | One or more items at or below reorder threshold |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read inventory files) |
| 10 | Unexpected error |

## Verification

After running, confirm:

- Exit code is 0 or 1 (not 2, 3, or 10)
- stdout is valid JSON (when using --format json)
- `data.items_scanned` > 0 (files were actually read)
- If exit code is 1, `findings` array is non-empty
