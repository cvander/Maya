---
name: vendor-order
description: Generate copy-paste-ready order text for a specific vendor.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [vendor, ordering, inventory, bar-ops]
    requires_tools: [terminal]
    config:
      - key: vendor
        description: "Vendor name to generate order for"
        default: ""
      - key: input_file
        description: "Path to vendor-order-review JSON output"
        default: ""
required_environment_variables: []
---

# Vendor Order

Takes vendor-order-review JSON output and a vendor name. Filters orders for that vendor and formats as copy-paste-ready plain text.

Read-only. Does not modify files or reach external services. No PII in output.

## When to Use

- After running vendor-order-review, to generate a specific vendor's order
- When preparing to email or call in an order
- Monday/Tuesday order placement workflow

## Procedure

Run the skill from the repo root:

```bash
# Generate order for a specific vendor
python -m skills.vendor_order --vendor "Southern Glazer's" --input-file /tmp/review.json --format json
```

Parse the JSON result:
- `status`: "ok" (no orders for vendor) or "warn" (order draft generated)
- `data.order_text`: plain text order ready to copy-paste
- `data.vendor`: matched vendor name
- `data.items_count`: number of items in the order

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No orders for specified vendor |
| 1 | Order draft generated |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read input) |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.order_text` is non-empty when status is "warn"
