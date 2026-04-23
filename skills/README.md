# Skills

Self-contained, callable units of work. Each skill runs on a Mac Mini and can be invoked via CLI or through Hermes orchestration.

See [CONTRACT.md](CONTRACT.md) for the skill contract: inputs, outputs, exit codes, manifest format, logging rules, and testing pattern.

## Usage

```bash
# Direct CLI invocation
python -m skills.<skill_name> [options]

# Standard flags
python -m skills.inventory_check --format json
python -m skills.inventory_check --inventory-dir path/to/fixtures

# Skill-specific flags (via extra_parser)
python -m skills.close_out --date 2026-04-12 --cash-count 1500 --card-total 3200 --expected 4700
python -m skills.eighty_six --add "Pliny the Elder" --reason "Keg kicked"
```

## Available Skills

### Inventory

| Skill | Status | Description |
|-------|--------|-------------|
| `inventory-check` | implemented | Scan current stock levels, flag low items |

### Vendors

| Skill | Status | Description |
|-------|--------|-------------|
| `vendor-order-review` | implemented | Review upcoming order needs across all vendors |
| `vendor-order` | implemented | Draft a copy-paste-ready order for a specific vendor |
| `vendor-contact` | implemented | Generate email body or phone script for a vendor |

### Scheduling

| Skill | Status | Description |
|-------|--------|-------------|
| `schedule-view` | implemented | Show the current week's schedule |
| `schedule-draft` | implemented | Draft next week's schedule with labor law flags |
| `schedule-notify` | implemented | Generate per-staff notification messages |

### Close-Out

| Skill | Status | Description |
|-------|--------|-------------|
| `close-out` | implemented | End-of-night cash reconciliation + tips + waste |
| `close-out-report` | implemented | Aggregate close-out data for a date range |
| `cost-analysis` | implemented | Pour cost, COGS, and margin analysis per drink |

### 86 List

| Skill | Status | Description |
|-------|--------|-------------|
| `eighty-six` | implemented | Manage items currently unavailable (add/remove/list) |

### Compliance

| Skill | Status | Description |
|-------|--------|-------------|
| `compliance-check` | implemented | Review upcoming compliance deadlines and cert expirations |
| `compliance-docs` | implemented | Check completeness of compliance documentation |

### Music

| Skill | Status | Description |
|-------|--------|-------------|
| `music-book` | implemented | Generate booking outreach for musicians |
| `music-calendar` | implemented | View and filter upcoming music schedule |

## Writing New Skills

Each skill is a Python package under `skills/`. Follow the contract in [CONTRACT.md](CONTRACT.md).

Use `skills/_skeleton/` as your starting template. It includes:

- `__main__.py` with `extra_parser` pattern for custom CLI args
- `main.py` with `run(ctx) -> Result` entry point
- `test_main.py` with golden-output test pattern
- `manifest.toml` and `SKILL.md` templates

Keep skills:

- **Single-purpose** - one skill, one job
- **CLI-friendly** - works from a terminal, returns clean output
- **Fail-safe** - the bar runs without them; failures log, not crash
- **Minimal dependencies** - stdlib only, runs on a Mac Mini with standard tools

### Hermes Discovery

If your skill will be invoked by Hermes orchestration (not just CLI), add a `SKILL.md` alongside `manifest.toml`. See [CONTRACT.md](CONTRACT.md) for the format.

- `manifest.toml` - runtime safety (what the skill is allowed to do)
- `SKILL.md` - orchestrator discovery (when and how to invoke the skill)
