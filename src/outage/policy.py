from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Account:
    account_id: str
    feeder: str
    life_safety: bool


@dataclass(frozen=True)
class Outage:
    outage_id: str
    feeder: str
    customers_affected: int
    minutes_open: int
    status: str


@dataclass(frozen=True)
class Ranked:
    outage_id: str
    feeder: str
    score: int
    crews: int
    reasons: tuple[str, ...]

    def render(self) -> str:
        reason_lines = "\n".join(f"- {reason}" for reason in self.reasons)
        return (
            f"Outage {self.outage_id} on {self.feeder} score {self.score}.\n"
            f"Suggest {self.crews} crew(s). This does not dispatch them and does not message customers.\n"
            f"{reason_lines}\n"
        )


def life_safety_feeders(accounts: list[Account]) -> set[str]:
    return {account.feeder for account in accounts if account.life_safety}


def rank_outages(outages: list[Outage], accounts: list[Account]) -> list[Ranked]:
    protected = life_safety_feeders(accounts)
    ranked: list[Ranked] = []
    for outage in outages:
        if outage.status != "open":
            continue
        score = 0
        reasons: list[str] = []
        if outage.feeder in protected:
            score += 100
            reasons.append("Life-safety account on this feeder (+100)")
        customer_points = min(40, outage.customers_affected // 10)
        duration_points = min(30, outage.minutes_open // 10)
        score += customer_points + duration_points
        reasons.append(f"{outage.customers_affected} customers affected (+{customer_points})")
        reasons.append(f"Open {outage.minutes_open} minutes (+{duration_points})")
        crews = 2 if score >= 100 else 1
        ranked.append(Ranked(outage.outage_id, outage.feeder, score, crews, tuple(reasons)))
    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked
