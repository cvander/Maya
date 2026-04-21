---
name: vendor-order-review
description: Parse inventory-check output and generate vendor order recommendations.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [vendor, ordering, inventory, bar-ops]
    requires_tools: [terminal]
    config:
      - key: input_file
        description: "Path to inventory-check JSON output"
        default: ""
required_environment_variables: []
---

# Vendor Order Review

Reads inventory-check JSON output and vendor docs. For each low-stock item, looks up the vendor and calculates order quantity (par - current qty). Groups orders by vendor.

Read-only. Does not modify files or reach external services. No PII in output.

## When to Use

- After running inventory-check and getting low stock warnings
- Sunday/Monday order planning workflow
- When preparing vendor orders for the week

## Procedure

Run the skill from the repo root:

```bash
# First run inventory-check to get low stock data
python -m skills.inventory_check --format json > /tmp/inventory.json

# Then review vendor orders
python -m skills.vendor_order_review --input-file /tmp/inventory.json --format json
```

Parse the JSON result:
- `status`: "ok" (no orders needed) or "warn" (orders to place)
- `findings`: array of ORDER_NEEDED items with vendor, item, and quantity
- `data.orders_by_vendor`: orders grouped by vendor name
- `data.total_items`: total items needing orders

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No orders needed |
| 1 | Orders needed for one or more vendors |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read input files) |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.orders_by_vendor` is populated when status is "warn"
