from outage.eval import run
from outage.ingest import EVALS_PATH, load_accounts, load_outages
from outage.policy import rank_outages


def test_eval_file_passes():
    assert run(EVALS_PATH) == 0


def test_life_safety_outranks_a_larger_commercial_outage():
    ranked = rank_outages(load_outages(), load_accounts())
    assert [item.outage_id for item in ranked] == ["OUT-1", "OUT-2"]
    assert ranked[0].score == 112
    assert ranked[0].crews == 2
    assert ranked[1].score == 43
    assert "does not message customers" in ranked[0].render()
