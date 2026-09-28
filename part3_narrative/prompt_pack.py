"""Deterministic offline template-fill logic for Part 4.
No LLM, network call, or API key is required.
"""


def fill_flagged_prompt(*, category: str, previous_revenue: float, current_revenue: float,
                        mom_pct: float, month: str, prev_month: str) -> str:
    """Fill the stakeholder template using only supplied verified values.

    The runner intentionally keeps the draft compact: category + exact MoM value.
    Revenue values remain available to the template contract but are not repeated,
    which makes numeric traceability easy to audit.
    """
    return (
        f"Context: {category} revenue was monitored for {month} vs. {prev_month}.\n"
        f"Insight (fact): {category} recorded {mom_pct}% MoM change.\n"
        f"Implication (hypothesis): Verify the category drivers and review the relevant "
        f"assortment, pricing, and operational changes before taking action."
    )
