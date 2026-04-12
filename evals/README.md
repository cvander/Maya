# Maya Eval Framework

Evaluation framework for Maya's 15 skills. Validates skill quality through deterministic offline tests and (placeholder) CI-only tests.

## Structure

```
evals/
  framework.py                     # Eval runner + scoring engine
  offline/                         # Deterministic, no API key needed
    test_skill_md_validity.py      # SKILL.md frontmatter and sections
    test_fixture_coverage.py       # Fixture directory completeness
    test_finding_codes.py          # Finding structure per CONTRACT.md
    test_exit_code_mapping.py      # Status/exit code consistency
  ci_only/                         # Require Hermes + API key (placeholders)
    hermes_invocation/             # Natural language -> skill routing
    schedule_quality/              # Schedule output quality
    vendor_completeness/           # Order list completeness
    compliance_accuracy/           # Cert/permit alert accuracy
```

## Running

### Offline evals (default)

Run all deterministic evals. No API key or Hermes needed.

```bash
python evals/framework.py --offline
```

Or directly with unittest:

```bash
python -m unittest discover -s evals/offline -p "test_*.py" -v
```

### CI-only evals

Placeholder specs. Will require Hermes + OPENROUTER_API_KEY when implemented.

```bash
python evals/framework.py --ci
```

### All evals

```bash
python evals/framework.py --all
```

## Offline Evals

### test_skill_md_validity
Validates every skill's SKILL.md:
- YAML frontmatter parses correctly
- Required fields present: name, description, version, author, license, platforms
- metadata.hermes section with tags and requires_tools/requires_toolsets
- Required markdown sections: When to Use, Procedure, Verification
- Procedure contains a `python -m skills.` command

### test_fixture_coverage
Validates fixture directory structure:
- Every skill has fixtures/ with happy_path/ containing expected.json
- Every skill has at least one warn/edge case fixture directory
- Minimum 2 fixture scenarios per skill

### test_finding_codes
Validates finding structure in expected.json files:
- Required keys: severity, code, subject, message
- Severity values: info, warn, fail
- Codes use UPPER_SNAKE_CASE format
- No duplicate code+subject within a scenario
- Non-empty subject and message strings

### test_exit_code_mapping
Validates status/exit code consistency:
- happy_path status is "ok" (exit 0)
- warn_case/low_stock status is "warn" (exit 1)
- All Result fields present per CONTRACT.md
- skill name matches manifest.toml
- findings is always a list
- metrics contains duration_ms

## CI-Only Evals

YAML scenario specs with placeholder scorers. Each defines:
- `eval_spec.yaml`: scoring method, pass threshold, requirements
- `scenarios/*.yaml`: input, expected output, scoring rubric
- `scorer.py`: placeholder scoring function

These will be implemented when Hermes integration is ready.

## Adding Evals

### Offline
Add a `test_*.py` file to `evals/offline/`. Use stdlib unittest. Discover skills dynamically via `SKILLS_DIR.glob("*/manifest.toml")`.

### CI-only
Add a new directory under `evals/ci_only/` with eval_spec.yaml, scenarios/, and scorer.py.
