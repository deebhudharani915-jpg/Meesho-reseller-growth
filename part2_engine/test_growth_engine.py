from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from part2_engine.growth_engine import is_flagged, mom_growth, validate_feed



def test_may_ethnic_wear_growth():
    # GIVEN April→May Ethnic Wear revenue moves 104520.77 -> 185107.61
    # WHEN evaluated by the growth engine
    # THEN growth is 77.1 and the category is flagged.
    pct = mom_growth(104520.77, 185107.61)
    assert pct == 77.1
    assert is_flagged(pct) == "flagged"


def test_june_beauty_growth():
    # GIVEN May→June Beauty & Personal Care revenue moves 35542.11 -> 37559.07
    # WHEN evaluated
    # THEN growth is 5.67 and it is not flagged.
    pct = mom_growth(35542.11, 37559.07)
    assert pct == 5.67
    assert is_flagged(pct) == "not_flagged"


def test_exact_boundary_escalates():
    # GIVEN previous=100000 and current=108000
    # WHEN evaluated
    # THEN exactly 8.0% is escalated for human review.
    pct = mom_growth(100000, 108000)
    assert pct == 8.0
    assert is_flagged(pct) == "escalate_exact_boundary"


def test_corrupted_feed_has_exact_three_errors_in_order():
    # GIVEN the supplied corrupted fixture
    # WHEN validate_feed runs
    # THEN exactly the three specified errors are returned in order.
    path = ROOT / "part2_engine" / "fixtures" / "corrupted_feed.csv"
    valid, errors = validate_feed(str(path))
    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_monthly_feed_passes():
    path = ROOT / "part2_engine" / "fixtures" / "monthly_category_revenue.csv"
    assert validate_feed(str(path)) == (True, [])


def test_full_may_table():
    expected = {
        "Ethnic Wear": 77.1,
        "Western Wear": -23.6,
        "Kids Wear": -23.48,
        "Home & Kitchen": -9.25,
        "Beauty & Personal Care": -12.75,
    }
    for category, pct in expected.items():
        assert mom_growth(
            {"Ethnic Wear": 104520.77, "Western Wear": 113866.15, "Kids Wear": 59847.27,
             "Home & Kitchen": 100446.23, "Beauty & Personal Care": 40737.01}[category],
            {"Ethnic Wear": 185107.61, "Western Wear": 86998.18, "Kids Wear": 45793.78,
             "Home & Kitchen": 91152.57, "Beauty & Personal Care": 35542.11}[category],
        ) == pct
        assert is_flagged(pct) == "flagged"


def test_full_june_table():
    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }
    previous = {"Ethnic Wear": 185107.61, "Western Wear": 86998.18, "Kids Wear": 45793.78,
                "Home & Kitchen": 91152.57, "Beauty & Personal Care": 35542.11}
    current = {"Ethnic Wear": 76371.53, "Western Wear": 97415.64, "Kids Wear": 56737.78,
               "Home & Kitchen": 129971.22, "Beauty & Personal Care": 37559.07}
    for category, (pct, status) in expected.items():
        actual = mom_growth(previous[category], current[category])
        assert actual == pct
        assert is_flagged(actual) == status


if __name__ == "__main__":
    tests = [
        test_may_ethnic_wear_growth,
        test_june_beauty_growth,
        test_exact_boundary_escalates,
        test_corrupted_feed_has_exact_three_errors_in_order,
        test_valid_monthly_feed_passes,
        test_full_may_table,
        test_full_june_table,
    ]
    for test in tests:
        test()
    print(f"{len(tests)} growth-engine tests passed")
