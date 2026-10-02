from __future__ import annotations

import sys

from outage.eval import run
from outage.ingest import load_accounts, load_outages
from outage.policy import rank_outages


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "eval":
        return run()
    for item in rank_outages(load_outages(), load_accounts()):
        print(item.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
