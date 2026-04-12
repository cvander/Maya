"""Placeholder scorer for compliance accuracy eval.

Not yet implemented - requires Hermes integration.
"""


def score(scenario: dict, actual: dict) -> dict:
    """Score a compliance-check result for accuracy.

    Args:
        scenario: The scenario spec (from YAML).
        actual: The actual compliance-check output.

    Returns:
        Dict with score (0-100), breakdown, and pass/fail.
    """
    raise NotImplementedError(
        "Compliance accuracy scorer requires Hermes integration. "
        "Run offline evals instead: python evals/framework.py --offline"
    )
