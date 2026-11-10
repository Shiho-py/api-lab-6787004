import uuid


# A duplicate username is refused with 400 and an error message.
def test_duplicate_username_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# Logging in with a wrong password is refused with 401.
def test_wrong_password_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    res = api.post("/api/users/token/login", json={**user, "password": "Wrong-Pizza-2026"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# An empty username is refused with 400 and an error message.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
