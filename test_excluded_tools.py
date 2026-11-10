import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [["Knife"], ["Scissors"], [], ["Knife", "Scissors"]],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding all tools should return 400 with a JSON error message.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools returns HTTP 500 with an empty body instead of 400 and a JSON error",
    strict=True,
    raises=AssertionError,
)
def test_excluding_all_tools_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    error = res.json()["error"]
    assert isinstance(error, str)
    assert error.strip()
