import uuid

import pytest
import requests

SITE = "https://quickpizza.grafana.com"


class QuickPizza(requests.Session):
    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault("timeout", 20)
        return super().request(method, SITE + url, *args, **kwargs)


@pytest.fixture(scope="session")
def api():
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201, res.text
    res = api.post("/api/users/token/login", json=user)
    assert res.status_code == 200, res.text
    return {"Authorization": "token " + res.json()["token"]}


@pytest.fixture
def auth(api):
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    res = api.post("/api/pizza", json={}, headers=auth)
    assert res.status_code == 200, res.text
    return res.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth)
    assert res.status_code == 201, res.text
    made = res.json()
    yield made
    res = api.delete(f"/api/ratings/{made['id']}", headers=auth)
    if res.status_code != 204:
        assert res.status_code == 400, res.text
        assert res.json() == {"error": f"rating ID {made['id']} not found"}
