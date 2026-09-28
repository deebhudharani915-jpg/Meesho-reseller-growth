# Meesho Reseller Growth & Alert Intelligence Pipeline

A local, deterministic four-part analytics project covering SQL computation, Python guardrails, reliable narrative drafting, and a human-reviewed mock agent workflow.

## Requirements

- Python 3.10+
- VS Code recommended
- No external packages are required for the core project. The test file can be run with `python part2_engine/test_growth_engine.py` if `pytest` is installed, or the assertions can be run with a standard Python test runner.
- No API keys, paid services, network calls, Gmail, SMTP, or hosted AI service are required.

## VS Code setup

1. Open the repository folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Run the commands below from the repository root.

## Run the complete project in order

### Part 1 — Generate data and SQL outputs

```bash
python data/generate_dataset.py
python part1_sql/run_queries.py
```

This creates:

- `data/resellers.csv` — 24 resellers.
- `data/orders.csv` — 900 orders.
- `data/meesho_reseller.db` — SQLite database.
- `part1_sql/output/monthly_category_revenue.csv` — 15 monthly-category rows used by Parts 2 and 4.
- Additional SQL result CSVs for region revenue, top resellers, inactive resellers, the LEFT JOIN count demonstration, and June Delivered AOV.

The seeded data is generated with `random.Random(42)` and the exact project specification.

### Part 2 — Guardrail and growth engine

```bash
python part2_engine/test_growth_engine.py
```

The test file uses ordinary Python `assert` statements, so no third-party test package is required. It is also compatible with pytest if you already use pytest locally.

The required corrupted fixture is:

```text
part2_engine/fixtures/corrupted_feed.csv
```

The validated Part 1 feed is copied to:

```text
part2_engine/fixtures/monthly_category_revenue.csv
```

### Part 3 — Narrative and masking checks

```bash
python part3_narrative/masking.py
```

The narrative deliverables are plain Markdown:

- `part3_narrative/prompt_pack.md`
- `part3_narrative/narrative_report.md`

The actual narrative template-fill function used by Part 4 is in:

- `part3_narrative/prompt_pack.py`

### Part 4 — Mock agent runner

May scenario:

```bash
python part4_agent/mock_agent_runner.py May \
  part2_engine/fixtures/april_category_revenue.csv \
  part2_engine/fixtures/may_category_revenue.csv
```

June scenario:

```bash
python part4_agent/mock_agent_runner.py June \
  part2_engine/fixtures/may_category_revenue.csv \
  part2_engine/fixtures/june_category_revenue.csv
```

For the required invalid-feed Hard Stop check:

```bash
python part4_agent/mock_agent_runner.py July \
  part2_engine/fixtures/monthly_category_revenue.csv \
  part2_engine/fixtures/corrupted_feed.csv
```

The runner prints exactly one structured JSON object. It never sends a message.

## Expected verified values

### May vs April

| Category | MoM | Status |
|---|---:|---|
| Ethnic Wear | 77.1% | flagged |
| Western Wear | -23.6% | flagged |
| Kids Wear | -23.48% | flagged |
| Home & Kitchen | -9.25% | flagged |
| Beauty & Personal Care | -12.75% | flagged |

### June vs May

| Category | MoM | Status |
|---|---:|---|
| Ethnic Wear | -58.74% | flagged |
| Western Wear | 11.97% | flagged |
| Kids Wear | 23.9% | flagged |
| Home & Kitchen | 42.59% | flagged |
| Beauty & Personal Care | 5.67% | not_flagged |

## How the Parts connect

**Part 1 → Part 2:** SQL computes the verified monthly category revenue first; Part 2 validates that feed and applies deterministic MoM growth and threshold rules.

**Part 2 → Part 3:** Verified growth values become the only numeric inputs to the narrative template. The prompt pack requires Context → Insight → Implication and prohibits invented figures.

**Part 3 → Part 4:** The agent runner uses the same Part 2 functions and the offline Part 3 template-fill function to draft messages. It caps drafts at three, suppresses the remainder for manual review, and separately records exact-boundary cases.

Overall, the project follows an **Intake → Summary → Report Draft → Validate** pattern: validate the input, compute verified facts, draft from those facts, then hold the result for human approval.

## Zero API keys

The entire pipeline runs with zero API keys, paid subscriptions, hosted services, or network calls. The AI narrative stage is intentionally deterministic and offline.

## Part 1 reference checks

- 24 resellers
- 900 orders
- 15 monthly-category rows
- Grand total revenue: INR 1262066.92
- Zero-order reseller: RS024
- June Delivered AOV: INR 1267.69
