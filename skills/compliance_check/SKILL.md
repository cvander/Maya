---
name: compliance-check
description: Scan compliance docs for expiring certs, overdue logs, and permit renewals.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [compliance, health, permits, certs, bar-ops]
    requires_tools: [terminal]
    config:
      - key: compliance_dir
        description: "Path to compliance markdown files"
        default: "docs/compliance"
      - key: days_ahead
        description: "Look-ahead window in days"
        default: "30"
required_environment_variables: []
---

# Compliance Check

Reads staff-certs.md, cooler-temps.md, pest-log.md, and permits/README.md. Checks for expiring certifications, overdue logs, and upcoming permit renewals. Reports findings by severity.

Read-only. Does not modify files or reach external services.

## When to Use

- Weekly compliance review (scheduled: Monday 9:00 AM)
- Before any scheduled inspection (ABC, SFDPH, SFFD)
- When onboarding new staff (check cert status)
- After receiving renewal notices from authorities

## Procedure

Run the skill from the repo root:

```bash
# Human-readable summary
python -m skills.compliance_check

# Structured JSON output (for automation)
python -m skills.compliance_check --format json

# Check with a specific reference date
python -m skills.compliance_check --date 2025-06-01 --format json

# Custom look-ahead window
python -m skills.compliance_check --days-ahead 60 --format json

# Against a custom compliance directory
python -m skills.compliance_check --compliance-dir path/to/compliance --format json
```

Parse the JSON result:

- `status`: "ok" (no issues) or "warn" (findings present)
- `findings`: array with codes CERT_EXPIRING, CERT_EXPIRED, LOG_OVERDUE, PERMIT_RENEWAL, INSPECTION_DUE
- `data.certs_checked`: number of staff certs scanned
- `data.logs_checked`: number of compliance logs scanned
- `data.permits_checked`: number of permits scanned

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All compliance items current |
| 1 | One or more compliance findings |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read compliance files) |
| 10 | Unexpected error |

## Verification

After running, confirm:

- Exit code is 0 or 1 (not 2, 3, or 10)
- stdout is valid JSON (when using --format json)
- `data.certs_checked` >= 0 (files were actually read)
- If exit code is 1, `findings` array is non-empty
