"""Placeholder scorer for schedule quality eval.

Not yet implemented - requires Hermes integration.
"""


def score(scenario: dict, actual: dict) -> dict:
    """Score a schedule-draft result for quality.

    Args:
        scenario: The scenario spec (from YAML).
        actual: The actual schedule-draft output.

    Returns:
        Dict with score (0-100), breakdown, and pass/fail.
    """
    raise NotImplementedError(
        "Schedule quality scorer requires Hermes integration. "
        "Run offline evals instead: python evals/framework.py --offline"
    )
