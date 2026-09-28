# Part 3.1 — Reusable Prompt Pack

## Trigger
Start this prompt only when a category's `is_flagged` result is exactly **`"flagged"`**. Exact-boundary cases (`"escalate_exact_boundary"`) are held for human review and do not use this drafting prompt.

## Input list
The template requires these verified placeholders:

- `{category}` — category name.
- `{previous_revenue}` — previous month's verified revenue.
- `{current_revenue}` — current month's verified revenue.
- `{mom_pct}` — verified MoM percentage from `mom_growth`.
- `{month}` — current month.
- `{prev_month}` — prior month, used explicitly in wording such as “May vs. April”.

## Prompt
```text
You are drafting a short internal stakeholder update for a regional manager.
Use ONLY the supplied placeholders below; do not calculate, infer, round, or invent
any additional numeric value.

Category: [{category}]
Previous revenue: [{previous_revenue}]
Current revenue: [{current_revenue}]
MoM percentage: [{mom_pct}]%
Current month: [{month}]
Previous month: [{prev_month}]

Write the update using exactly this structure:
Context: State what is being measured and the period comparison.
Insight (fact): State the supplied MoM percentage exactly and identify the category.
Implication (hypothesis): Give one specific next action. If you propose a cause,
label it as a hypothesis because the supplied data does not prove causation.

Never state a number that is not one of the supplied placeholders. Do not expose
raw reseller names; use region plus the approved reseller alias when reseller
information is present.
```

## Checklist
Before the draft is used, verify all of the following:

1. **Numeric traceability:** every number in the draft exactly matches a supplied placeholder value; no new numeric figure appears.
2. **Structure:** the draft contains Context, Insight, and Implication sections.
3. **Fact/hypothesis labeling:** the MoM result is explicitly labeled as a fact; any proposed cause is explicitly labeled as a hypothesis.
4. **Actionability:** the implication names a concrete next check or action rather than saying only “look into it”.
5. **Period accuracy:** `{month}` and `{prev_month}` are named correctly and in the right direction.
6. **Privacy:** if reseller information is included, only the approved alias and region are used; no raw reseller name appears.
7. **Threshold integrity:** the prompt is not used for `not_flagged` or `escalate_exact_boundary` categories.
