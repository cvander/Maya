---
name: vendor-contact
description: Generate email body or phone script for contacting a vendor.
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
        description: "Vendor name to contact"
        default: ""
      - key: method
        description: "Contact method: email or phone"
        default: "email"
required_environment_variables: []
---

# Vendor Contact

Reads vendor docs and generates a contact draft (email body or phone script) for a specific vendor. Includes rep name, account number, and placeholder for order details.

Read-only. Does not modify files or reach external services. No PII in output.

## When to Use

- When placing an order by email or phone
- After vendor-order generates the order text
- When contacting a vendor for the first time

## Procedure

Run the skill from the repo root:

```bash
# Generate email draft
python -m skills.vendor_contact --vendor "Southern Glazer's" --method email --format json

# Generate phone script
python -m skills.vendor_contact --vendor "Anchor Distributing" --method phone --format json
```

Parse the JSON result:

- `status`: "ok" (vendor not found) or "warn" (draft generated)
- `data.message`: the email body or phone script text
- `data.contact_info`: vendor contact details (rep, phone, email)
- `data.method`: the contact method used

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Vendor not found |
| 1 | Contact draft generated |
| 2 | Config error (bad arguments) |
| 3 | Data error (can't read vendor docs) |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.message` is non-empty when status is "warn"
