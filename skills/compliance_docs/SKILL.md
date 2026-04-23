---
name: compliance-docs
description: Audit compliance documentation for completeness and freshness.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [compliance, docs, audit, bar-ops]
    requires_tools: [terminal]
    config:
      - key: compliance_dir
        description: "Path to compliance markdown files"
        default: "docs/compliance"
required_environment_variables: []
---

# Compliance Docs

Reads all compliance markdown files and permits/README.md. Reports which expected docs exist, which are missing, which are empty, and which are stale (not updated in >30 days).

Read-only. Does not modify files or reach external services. No PII in output.

## When to Use

- Monthly documentation audit (scheduled: 1st of month)
- Before any scheduled inspection (to verify docs are in order)
- When onboarding a new manager (verify all docs exist)
- After setting up a new bar location

## Procedure

Run the skill from the repo root:

```bash
# Human-readable summary
python -m skills.compliance_docs

# Structured JSON output (for automation)
python -m skills.compliance_docs --format json

# Against a custom compliance directory
python -m skills.compliance_docs --compliance-dir path/to/compliance --format json
```

Parse the JSON result:

- `status`: "ok" (all docs present and current) or "warn" (findings present)
- `findings`: array with codes DOC_MISSING, DOC_EMPTY, DOC_STALE
- `data.docs_checked`: number of docs audited
- `data.docs_present`: number of docs found
- `data.docs_missing`: number of expected docs not found

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All expected docs present and current |
| 1 | One or more documentation issues |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read directory) |
| 10 | Unexpected error |

## Verification

After running, confirm:

- Exit code is 0 or 1 (not 2, 3, or 10)
- stdout is valid JSON (when using --format json)
- `data.docs_checked` > 0 (directory was actually read)
- If exit code is 1, `findings` array is non-empty
