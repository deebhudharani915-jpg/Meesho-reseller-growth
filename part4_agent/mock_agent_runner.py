import csv
import json
import sys
from pathlib import Path

# Support both `python -m part4_agent.mock_agent_runner` and direct script execution.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed
from part3_narrative.prompt_pack import fill_flagged_prompt


def _rows(path: str) -> dict[str, float]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["category"].strip(): float(row["revenue"]) for row in reader}


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Run the guarded offline monitoring workflow and return one JSON-ready object."""
    valid, errors = validate_feed(current_month_csv)
    result = {
        "run_month": month,
        "validation_status": "valid" if valid else "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "drafted_and_held_for_approval" if valid else "hard_stop",
    }
    if not valid:
        return result

    previous = _rows(previous_month_csv)
    current = _rows(current_month_csv)
    candidates = []
    for category, current_revenue in current.items():
        if category not in previous:
            continue
        previous_revenue = previous[category]
        pct = mom_growth(previous_revenue, current_revenue)
        status = is_flagged(pct)
        if status == "flagged":
            candidates.append((category, pct, previous_revenue, current_revenue))
        elif status == "escalate_exact_boundary":
            result["escalated_categories"].append(category)

    candidates.sort(key=lambda x: abs(x[1]), reverse=True)
    for index, (category, pct, previous_revenue, current_revenue) in enumerate(candidates):
        if index < 3:
            message = fill_flagged_prompt(
                category=category,
                previous_revenue=previous_revenue,
                current_revenue=current_revenue,
                mom_pct=pct,
                month=month,
                prev_month=_previous_month(month),
            )
            result["flagged_categories"].append({
                "category": category,
                "mom_pct": pct,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
                "drafted": True,
                "message": message,
            })
        else:
            result["suppressed_categories"].append(category)
    return result


def _previous_month(month: str) -> str:
    order = {"May": "April", "June": "May"}
    return order.get(month, "previous month")


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("Usage: python part4_agent/mock_agent_runner.py <month> <previous.csv> <current.csv>")
    print(json.dumps(run(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2))


if __name__ == "__main__":
    main()
