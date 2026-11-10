import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201, res.text
    made = res.json()
    try:
        assert made["stars"] == 3
        assert made["pizza_id"] == pizza_id
    finally:
        deleted = api.delete(f"/api/ratings/{made['id']}", headers=auth)
        assert deleted.status_code == 204, deleted.text


@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


@pytest.mark.parametrize(
    "stars, error",
    [
        (3.5, "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"),
        ("3", "json: cannot unmarshal string into Go struct field Rating.stars of type int"),
    ],
    ids=["decimal", "text"],
)
def test_stars_invalid_type(api, auth, pizza_id, stars, error):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": error}


def test_missing_stars_is_refused(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


def test_nonexistent_pizza_is_refused(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


def test_missing_token_is_refused(api, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


def test_short_token_is_refused(api, pizza_id):
    res = api.post(
        "/api/ratings",
        json={"pizza_id": pizza_id, "stars": 3},
        headers={"Authorization": "token short"},
    )
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
