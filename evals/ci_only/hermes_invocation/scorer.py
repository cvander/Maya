"""Placeholder scorer for Hermes invocation eval.

Not yet implemented - requires Hermes integration.
"""


def score(scenario: dict, actual: dict) -> dict:
    """Score a single scenario result.

    Args:
        scenario: The scenario spec (from YAML).
        actual: The actual Hermes response (skill invoked, args passed).

    Returns:
        Dict with score (0-100), breakdown, and pass/fail.
    """
    raise NotImplementedError(
        "Hermes invocation scorer requires Hermes integration. "
        "Run offline evals instead: python evals/framework.py --offline"
    )
