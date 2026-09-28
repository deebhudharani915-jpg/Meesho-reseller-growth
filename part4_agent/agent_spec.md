# Part 4.1 — Agent Specification

## Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it is considered sent.

## Tools
The agent uses:

- `part2_engine.growth_engine.validate_feed` — input guardrail.
- `part2_engine.growth_engine.mom_growth` — deterministic MoM calculation.
- `part2_engine.growth_engine.is_flagged` — threshold decision with exact-boundary escalation.
- `part3_narrative.prompt_pack.fill_flagged_prompt` — deterministic offline narrative template fill.

No network call, API key, Gmail, SMTP, or external LLM is required.

## Memory / State
Between runs, the system needs the previous month's verified revenue per category so the next run can calculate MoM. In this mock implementation that state is represented by `previous_month_csv`; no hidden state or external database is required.

## Planner
1. Load the monthly revenue feed and run `validate_feed`.
2. If invalid, Hard Stop and report validation errors.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by `abs(mom_pct)` descending.
6. Draft a message for at most the top 3 flagged categories using Part 3's template-fill function.
7. Log any remaining flagged categories beyond the cap as `suppressed, review manually` without drafting a message.
7b. Separately log any `escalate_exact_boundary` category into `escalated_categories`; never draft it and never silently drop it.
8. Emit one structured JSON object per run.

## Feedback Loop
Every drafted message is held for human approval. The runner represents this by `action_taken = "drafted_and_held_for_approval"`; it never sends an email or message.

## Guardrails

### Input guardrail
`validate_feed` must pass before any MoM computation or narrative drafting begins. A failed validation is a **Hard Stop**.

### Action guardrail
No message is ever auto-sent. The agent only drafts and holds messages for approval.

### Output guardrail
Every number in a drafted message must trace to a verified Part 1/Part 2 value. The deterministic template-fill function receives only verified values and does not calculate or invent new numbers.

## Stopping conditions

- **Success:** drafts are produced when categories cross the threshold, or correctly zero drafts are produced when nothing crosses it; all emitted numbers are traceable.
- **Hard Stop:** `validate_feed` returns `False`. The validation errors are surfaced in `validation_errors`; no MoM computation is attempted and no draft is created.

## Given–When–Then agent specifications

### 1. May Ethnic Wear
**GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** the agent runs `mom_growth` then `is_flagged` on it, **THEN** `mom_growth` returns `77.1` and `is_flagged` returns `"flagged"`.

### 2. June Beauty & Personal Care
**GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** the agent evaluates it, **THEN** `mom_growth` returns `5.67` and `is_flagged` returns `"not_flagged"`.

### 3. Exact boundary
**GIVEN** a synthetic pair `previous=100000, current=108000` (chosen so the growth is exactly on the threshold boundary), **WHEN** the agent evaluates it, **THEN** `mom_growth` returns exactly `8.0` and `is_flagged` returns `"escalate_exact_boundary"` — not `"flagged"` and not `"not_flagged"`.

### 4. Corrupted feed
**GIVEN** the corrupted feed fixture, **WHEN** the agent runs `validate_feed`, **THEN** it returns `(False, errors)` where `errors` has exactly 3 entries, matching in order: the negative-revenue row, the missing-category row, and the missing-revenue row; the agent Hard Stops with no flagged or suppressed categories.

## Structured output contract
Every run returns exactly these top-level keys:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`

Each drafted flagged object contains `category`, `mom_pct`, `previous_revenue`, `current_revenue`, `drafted`, and `message`.
