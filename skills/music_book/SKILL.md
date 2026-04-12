---
name: music-book
description: Generate outreach messages for booking artists.
version: 0.1.0
author: Maya
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [music, booking, entertainment, bar-ops]
    requires_toolsets: [terminal]
    config:
      - key: music.dir
        description: "Path to music data directory"
        default: "docs/music"
required_environment_variables: []
---

# Music Book

Generate outreach messages (email or phone script) for booking artists at the bar.

## When to Use

- When Maya needs to reach out to an artist for booking
- When checking for date conflicts before booking
- When generating a draft booking email or phone script

## Procedure

```bash
python -m skills.music_book --artist "The Slow Drags" --date 2026-04-25 --method email --format json
```

### Arguments

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--artist NAME` | yes | - | Artist name to book |
| `--date YYYY-MM-DD` | yes | - | Date to book |
| `--method email\|phone` | no | email | Outreach method |
| `--music-dir PATH` | no | docs/music | Override music data directory |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | OK - booking draft generated, no conflicts |
| 1 | Warnings - date conflict found or artist not found |
| 2 | Config error |
| 3 | Data error |
| 10 | Unexpected error |

## Verification

- Exit code is 0 or 1
- stdout is valid JSON (with --format json)
- `data.message` contains the outreach draft
- `data.artist_info` contains artist details
- `data.conflict` is null or contains conflict details
