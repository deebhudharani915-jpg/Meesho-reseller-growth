def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    return not any(name and name in text for name in reseller_names)


if __name__ == "__main__":
    assert alias_for("RS019") == "ALIAS-19"
    names = ["Mumbai Reseller 1", "Mumbai Reseller 4", "Hyderabad Reseller 6",
             "Lucknow Reseller 6", "Jaipur Reseller 5"]
    safe = "West — ALIAS-19; West — ALIAS-22; South — ALIAS-12; North — ALIAS-06; North — ALIAS-05."
    unsafe = "West — Mumbai Reseller 1."
    assert assert_no_raw_names_leak(safe, names) is True
    assert assert_no_raw_names_leak(unsafe, names) is False
    print("masking checks passed")
