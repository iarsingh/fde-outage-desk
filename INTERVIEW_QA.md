# fde-outage-desk — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-outage-desk address, and what can you demonstrate?

Simulated forward deployed engagement for Cedar Grid, a regional utility. The storm desk was sorting outages by customer count. A feeder with a registered life-safety account was waiting behind a larger commercial outage. The control room will not let this tool text customers or dispatch a crew by itself.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/outage/eval.py`](src/outage/eval.py): Implementation or supporting configuration.
- [`src/outage/policy.py`](src/outage/policy.py): Implementation or supporting configuration.
- [`src/outage/ingest.py`](src/outage/ingest.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/outage/__init__.py`](src/outage/__init__.py): Implementation or supporting configuration.
- [`src/outage/__main__.py`](src/outage/__main__.py): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.
- [`tests/test_policy.py`](tests/test_policy.py): Executable checks and regression examples.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `run` and explain the decision it makes?

The main walkthrough here is `run(path: Path | None=None)` in [`src/outage/eval.py`](src/outage/eval.py#L9).

```python
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
```

This is an excerpt; follow the source link for the rest of the branches.

The implementation calls `failures.append`, `item.render`, `len`, `load_accounts`, `load_cases`, `load_outages`, `print`, `rank_outages`, `ranked.get`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `rank_outages` have?

`rank_outages(outages: list[Outage], accounts: list[Account])` is defined in [`src/outage/policy.py`](src/outage/policy.py#L43).

Its return expressions include:

- `ranked`

It uses `Ranked`, `life_safety_feeders`, `min`, `ranked.append`, `ranked.sort`, `reasons.append`, `tuple`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `SystemExit(main())` in [`src/outage/__main__.py`](src/outage/__main__.py#L19).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_policy.py`](tests/test_policy.py#L6) contains `test_eval_file_passes`:

```python
def test_eval_file_passes():
    assert run(EVALS_PATH) == 0
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. How do you separate the current design from a future production design?

The current design is the source/component map in [PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md). A future deployment needs explicit input contracts, persistence decisions, authentication, monitoring, and rollback. I would present these as proposed work until the corresponding implementation and verification exist.

## 8. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `run`?

In [`src/outage/eval.py`](src/outage/eval.py#L9), `run(path: Path | None=None)` receives the inputs. The function computes these intermediate values:

- `ranked = {item.outage_id: item for item in rank_outages(load_outages(), load_accounts())}`
- `failures = []`
- `cases = load_cases(path)`
- `order = [item.outage_id for item in rank_outages(load_outages(), load_accounts())]`

Its result is defined by:

- `0`
- `1`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/outage/eval.py`](src/outage/eval.py#L9) branches on:

- `order and order != ['OUT-1', 'OUT-2']`
- `failures`
- `case['expected'] == 'excluded'`
- `item is None`
- `item.score != case['expected_score']`
- `'message customers' not in item.render()`
- `item is not None`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
