# Cedar Grid outage desk

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/outage/eval.py`](src/outage/eval.py) | Functions: `run` |
| [`src/outage/policy.py`](src/outage/policy.py) | Functions: `life_safety_feeders`, `rank_outages`, `render` |
| [`src/outage/ingest.py`](src/outage/ingest.py) | Functions: `load_accounts`, `load_outages`, `load_cases` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`src/outage/__init__.py`](src/outage/__init__.py) | Implementation or supporting configuration |
| [`src/outage/__main__.py`](src/outage/__main__.py) | Functions: `main` |
| [`Dockerfile`](Dockerfile) | Container build/service configuration |
| [`tests/test_policy.py`](tests/test_policy.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |
| [`docs/01-discovery.md`](docs/01-discovery.md) | Project explanations or operating notes |
| [`docs/02-security.md`](docs/02-security.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

<!-- project-guide:end -->

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

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```
