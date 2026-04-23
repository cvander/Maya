# CI-Only Evals

These evaluations require a running Hermes instance and an OPENROUTER_API_KEY.
They are not run in offline mode.

## Structure

Each eval directory contains:

- `eval_spec.yaml` - Evaluation definition (scoring method, threshold, requirements)
- `scenarios/` - Individual test scenarios as YAML files
- `scorer.py` - Placeholder scoring logic (to be implemented with Hermes integration)

## Evals

### hermes_invocation

Tests that Hermes correctly routes natural language queries to the right Maya skill
with the correct arguments.

### schedule_quality

Tests that schedule-draft produces reasonable schedules given staff and event inputs.

### vendor_completeness

Tests that vendor-order-review produces complete order lists from known inventory states.

### compliance_accuracy

Tests that compliance-check correctly identifies expiring certs and overdue items.

## Running

These evals are placeholder specs only. When Hermes integration is ready:

```bash
python evals/framework.py --ci
```
