from __future__ import annotations

from pathlib import Path

from outage.ingest import load_accounts, load_cases, load_outages
from outage.policy import rank_outages


def run(path: Path | None = None) -> int:
    ranked = {item.outage_id: item for item in rank_outages(load_outages(), load_accounts())}
    failures = []
    cases = load_cases(path)
    for case in cases:
        item = ranked.get(case["outage_id"])
        if case["expected"] == "excluded":
            if item is not None:
                failures.append(f"{case['outage_id']} was ranked")
            continue
        if item is None:
            failures.append(f"{case['outage_id']} missing")
            continue
        if item.score != case["expected_score"]:
            failures.append(f"{case['outage_id']}: score {item.score}")
        if "message customers" not in item.render():
            failures.append(f"{case['outage_id']}: missing customer-message refusal")
    order = [item.outage_id for item in rank_outages(load_outages(), load_accounts())]
    if order and order != ["OUT-1", "OUT-2"]:
        failures.append(f"order {order}")
    if failures:
        print(f"{len(failures)} eval failure(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"{len(cases)} eval cases passed")
    return 0
