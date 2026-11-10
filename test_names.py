import requests

SITE = "https://quickpizza.grafana.com"


def test_names_are_listed():
    res = requests.get(SITE + "/api/names", timeout=20)
    assert res.status_code == 200
    assert "Margherita" in res.json()["names"]
