from app.tasks import long_running_task

def test_task_runs():
    res = long_running_task({"n": 1})
    assert "computed_total" in res
    assert res["input"]["n"] == 1
