---
name: eighty-six
description: Manage the 86 list of currently unavailable items.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [86, out-of-stock, inventory, bar-ops, real-time]
    requires_tools: [terminal]
    config:
      - key: data_dir
        description: "Path to 86 list data directory"
        default: "data/86"
required_environment_variables: []
---

# Eighty-Six

Manage the 86 list of currently unavailable items. Add items when they run out, remove them when restocked, and list what is currently unavailable.

Idempotent. Writes only to data/86/current.md. No PII in output.

## When to Use

- When a bartender reports an item is out (86 it)
- When a delivery arrives and restocks an item (un-86 it)
- Before service to check what is currently unavailable
- When a guest asks about availability

## Procedure

Run the skill from the repo root:

```bash
# List currently 86'd items (default behavior)
python -m skills.eighty_six --format json

# Explicitly list
python -m skills.eighty_six --list --format json

# Add an item to the 86 list
python -m skills.eighty_six --add "Pliny the Elder" --reason "Keg kicked" --reported-by "Alex" --format json

# Remove an item (back in stock)
python -m skills.eighty_six --remove "Pliny the Elder" --format json
```

Parse the JSON result:
- `status`: "ok" (all clear or action completed) or "warn" (items on 86 list)
- `findings`: array with CURRENTLY_86D, ITEM_86D, or ITEM_BACK codes
- `data.items`: list of currently 86'd items (on --list)
- `data.count`: number of 86'd items (on --list)

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK - action completed or no items 86'd |
| 1 | Warn - items currently on the 86 list |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read/write data file) |
| 10 | Unexpected error |

## Verification

After running, confirm:
- Exit code is 0 or 1 (not 2, 3, or 10)
- stdout is valid JSON (when using --format json)
- For --add: item appears in subsequent --list
- For --remove: item no longer appears in --list
