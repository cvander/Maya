# Contributing to Maya

Maya is a public research project. If you're running a bar, a restaurant, or any traditional business and want to explore what AI can do for your operations, we want to hear from you.

## Before You Start

Read these files to understand the project:

- **[SOUL.md](SOUL.md)** - Who Maya is (identity, personality, voice)
- **[AGENTS.md](AGENTS.md)** - How Maya operates (rules, boundaries, red lines)
- **[DREAMS.md](DREAMS.md)** - Where Maya is headed

If SOUL.md and AGENTS.md ever conflict: SOUL.md wins on character, AGENTS.md wins on operations.

## Development Setup

Maya runs on a Mac Mini behind a bar. Keep that in mind for everything you build.

### Prerequisites

- macOS (tested on Mac Mini)
- [OpenClaw](https://openclaw.org)
- [Hermes](https://hermes.org)
- [Claude Code](https://claude.ai/code) CLI

### Getting Started

```bash
git clone https://github.com/cvander/Maya.git
cd Maya

# Copy and configure
cp config/openclaw/config.example.yaml config/openclaw/config.yaml
cp config/hermes/config.example.yaml config/hermes/config.yaml

# Edit configs with your values - never commit credentials
```

## How to Contribute

### Reporting Bugs

Open an [issue](https://github.com/cvander/Maya/issues/new?template=bug_report.yml) with:

- What happened vs. what you expected
- Steps to reproduce
- Your environment (Mac Mini? local dev?)

### Suggesting Features or Skills

Open an [issue](https://github.com/cvander/Maya/issues/new?template=feature_request.yml) describing:

- What problem it solves
- Which Maya domain it touches (inventory, vendors, scheduling, music, compliance, menu)
- Why it belongs in Maya (read AGENTS.md hard stops first)

### Pull Requests

1. Fork the repo and create a feature branch (`git checkout -b my-feature`)
2. Make your changes
3. Test locally on macOS before pushing
4. Open a PR with a clear description of what changed and why

## Writing Skills

Skills live in `skills/` as standalone scripts. Follow this pattern:

```bash
#!/bin/bash
# skill: skill-name
# description: What this skill does
# usage: maya skill-name [options]

set -euo pipefail

# Skill logic here
```

Skills must be:

- **Single-purpose** - one skill, one job
- **CLI-friendly** - works from a terminal, returns clean output
- **Fail-safe** - the bar runs without them; failures log, not crash
- **Minimal dependencies** - runs on a Mac Mini with standard tools

## What NOT to Contribute

Read the hard stops in [AGENTS.md](AGENTS.md). These are non-negotiable:

- No franchising, scaling, or "second location" features
- No QR code menus, apps, or loyalty programs
- No social media strategy tools
- No features that profile or extract insights from regulars' personal information

## Privacy

Maya handles real bar operations. The bar holds confidences.

- Never log, export, or analyze personal information about regulars
- No profiling, no patterns, no "insights" from people's conversations
- If your contribution touches any personal data, think twice, then think again

## Style

- Write for clarity, not cleverness
- Keep dependencies minimal
- Credentials go in environment variables, never in config files
- `trash` > `rm` - move files, don't delete them

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md). Be decent.
