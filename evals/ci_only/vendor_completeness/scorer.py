"""Placeholder scorer for vendor completeness eval.

Not yet implemented - requires Hermes integration.
"""


def score(scenario: dict, actual: dict) -> dict:
    """Score a vendor-order-review result for completeness.

    Args:
        scenario: The scenario spec (from YAML).
        actual: The actual vendor-order-review output.

    Returns:
        Dict with score (0-100), breakdown, and pass/fail.
    """
    raise NotImplementedError(
        "Vendor completeness scorer requires Hermes integration. "
        "Run offline evals instead: python evals/framework.py --offline"
    )
