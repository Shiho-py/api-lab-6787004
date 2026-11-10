import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}


def test_tools_are_listed():
    res = requests.get(SITE + "/api/tools", headers=AUTH, timeout=20)
    assert res.status_code == 200
    assert res.json() == {"tools": ["Knife", "Pizza cutter", "Scissors"]}
