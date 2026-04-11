# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Maya, please report it responsibly.

**Do not open a public issue.** Instead:

1. Use [GitHub's private vulnerability reporting](https://github.com/cvander/Maya/security/advisories/new)
2. Or email the maintainer directly (see GitHub profile for contact)

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

You'll receive acknowledgment within 48 hours. We'll work with you on a fix before any public disclosure.

## What's in Scope

Maya is designed to run on a Mac Mini behind a bar, unattended. Security matters here because:

- The system handles bar operations data (inventory, vendor contacts, scheduling)
- It may run 24/7 with remote access via Tailscale or similar
- Privacy commitments to regulars are non-negotiable (see [AGENTS.md](AGENTS.md))

Relevant areas:

- Credential handling in configs and environment variables
- Remote access and network exposure
- Data leakage of personal information
- Skill scripts that could be exploited
- OpenClaw/Hermes configuration weaknesses

## What's NOT in Scope

- Theoretical attacks that require physical access to the Mac Mini behind the bar
- Vulnerabilities in upstream dependencies (OpenClaw, Hermes) - report those to their maintainers
- Social engineering attacks on bar staff

## Supported Versions

This project is pre-release. Security fixes apply to the `main` branch only.
