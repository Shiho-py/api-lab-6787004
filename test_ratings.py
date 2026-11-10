# A new rating comes back with an id, its stars and its pizza.
def test_create_rating(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    body = res.json()
    try:
        assert body["stars"] == 5
        assert body["pizza_id"] == pizza_id
        assert isinstance(body["id"], int)
    finally:
        deleted = api.delete(f"/api/ratings/{body['id']}", headers=auth)
        assert deleted.status_code == 204, deleted.text


# A saved rating can be read back by its id.
def test_read_rating(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Changing a rating's stars returns the new number of stars.
def test_update_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 4}, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == 4


# A deleted rating can no longer be read.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=auth)
    assert res.status_code == 204
    res = api.get(path, headers=auth)
    assert res.status_code == 404
