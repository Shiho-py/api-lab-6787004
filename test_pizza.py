import requests

SITE = "https://quickpizza.grafana.com"
AUTH = {"Authorization": "token abcdef0123456789"}
VEGETARIAN = {"mustBeVegetarian": True}


# A vegetarian request gets a named pizza with vegetarian ingredients only.
def test_vegetarian_pizza():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN, headers=AUTH, timeout=20)
    assert res.status_code == 200
    body = res.json()
    assert body["pizza"]["name"] != ""
    for ingredient in body["pizza"]["ingredients"]:
        assert ingredient["vegetarian"] is True, ingredient["name"]


# A request without a token is refused with 401 and an error message.
def test_pizza_without_token_is_refused():
    res = requests.post(SITE + "/api/pizza", json=VEGETARIAN, timeout=20)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
