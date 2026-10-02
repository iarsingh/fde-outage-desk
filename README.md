# Cedar Grid outage desk

Simulated forward deployed engagement for Cedar Grid, a regional utility. The storm desk was sorting outages by customer count. A feeder with a registered life-safety account was waiting behind a larger commercial outage. The control room will not let this tool text customers or dispatch a crew by itself.

## What the desk gets

| Outage | Feeder | Score | Why |
| --- | --- | --- | --- |
| OUT-1 | F-12, life-safety account | 112 | +100 life safety, 40 customers (+4), 80 minutes (+8). Suggest 2 crews |
| OUT-2 | F-4, 400 customers | 43 | no life-safety account, +40 customers, +3 minutes. Suggest 1 crew |
| OUT-3 | restored | excluded | not in the open queue |

Life safety beats a ten-times-larger customer count. The sentence on every card is that this does not dispatch and does not message customers.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest
python -m outage eval
python -m outage
```

## Docs

- [Discovery](docs/01-discovery.md)
- [Security](docs/02-security.md)
- [Readout](docs/03-readout.md)

The pilot does not claim fewer outage minutes. It claims the life-safety feeder is first, and no customer message is sent.
