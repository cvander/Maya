# Skills

Self-contained, callable units of work. Each skill runs on a Mac Mini and can be invoked via CLI or through Hermes orchestration.

## Usage

```bash
# Direct CLI invocation
maya <skill-name> [options]

# List available skills
maya --list

# Via Hermes orchestration (planned)
hermes run <skill-name> [options]

# Via Claude Code (planned)
/skill <skill-name>
```

## Available Skills

### Implemented

| Skill | Description | Usage |
|-------|-------------|-------|
| `close-out` | End-of-night cash count and reconciliation | `maya close-out [--date YYYY-MM-DD]` |

### Planned

| Skill | Description |
|-------|-------------|
| `inventory-check` | Scan current stock levels, flag low items |
| `inventory-count` | Full count workflow with variance tracking |
| `inventory-report` | Generate inventory summary for a date range |
| `vendor-order` | Draft and send an order to a specific vendor |
| `vendor-order-review` | Review upcoming order needs across all vendors |
| `vendor-contact` | Send a message to a vendor (email or phone) |
| `schedule-view` | Show the current week's schedule |
| `schedule-draft` | Draft next week's schedule based on patterns |
| `schedule-notify` | Send schedule to staff |
| `close-out-report` | Generate close-out summary for a date range |
| `music-book` | Reach out to a musician for booking |
| `music-calendar` | View upcoming live music schedule |
| `compliance-check` | Review upcoming compliance deadlines |
| `compliance-docs` | Gather and organize compliance documents |

## Writing New Skills

Each skill is a standalone script in this directory. Follow this pattern:

```bash
#!/bin/bash
# skill: skill-name
# description: What this skill does
# usage: maya skill-name [options]

set -euo pipefail

# Skill logic here
```

Keep skills:
- **Single-purpose** - one skill, one job
- **CLI-friendly** - works from a terminal, returns clean output
- **Fail-safe** - the bar runs without them; failures log, not crash
- **Minimal dependencies** - runs on a Mac Mini with standard tools
