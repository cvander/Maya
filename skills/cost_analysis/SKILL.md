---
name: cost-analysis
description: "Calculate pour costs and margins from menu and inventory data."
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [cost, margin, pour-cost, menu, inventory, analysis]
    requires_toolsets: [terminal]
    config: []
required_environment_variables: []
---

# Cost Analysis

Reads the current menu and inventory files to calculate pour cost per drink, category COGS, and margin percentages. Flags items with high pour costs (>30%) or low margins (<$8).

## When to Use

- When reviewing menu pricing decisions
- Before adjusting prices on cocktails or spirits
- Monthly cost analysis for the bar

## Procedure

```bash
python -m skills.cost_analysis --format json
python -m skills.cost_analysis --format json --category cocktails
```

Optional: `--category all|beer|spirits|wine|cocktails` (defaults to all).

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK, all margins healthy |
| 1 | Warnings: high pour cost or low margin items |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.items` contains analyzed menu items with cost/margin data
