from __future__ import annotations

import csv
import json
from pathlib import Path

from outage.policy import Account, Outage

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
EVALS_PATH = ROOT / "evals" / "questions.jsonl"


def load_accounts() -> list[Account]:
    with (DATA_DIR / "accounts.csv").open(newline="") as handle:
        return [
            Account(row["account_id"], row["feeder"], row["life_safety"].strip().lower() == "yes")
            for row in csv.DictReader(handle)
        ]


def load_outages() -> list[Outage]:
    with (DATA_DIR / "outages.csv").open(newline="") as handle:
        return [
            Outage(
                row["outage_id"],
                row["feeder"],
                int(row["customers_affected"]),
                int(row["minutes_open"]),
                row["status"],
            )
            for row in csv.DictReader(handle)
        ]


def load_cases(path: Path | None = None) -> list[dict]:
    return [json.loads(line) for line in (path or EVALS_PATH).read_text().splitlines() if line.strip()]
