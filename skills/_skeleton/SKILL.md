---
name: <skill-name>
description: <One-line description.>
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: []
    requires_toolsets: [terminal]
    config: []
required_environment_variables: []
---

# <Skill Name>

<Brief description of what the skill does.>

## When to Use

- <Trigger condition 1>
- <Trigger condition 2>

## Procedure

```bash
python -m skills.<skill_name> --format json
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK |
| 1 | Warnings/findings present |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data` field is populated
