import pytest

from test_create_rating import STARS_ERROR


# Updates save 1 or 5 stars; rejected values leave the rating unchanged.
@pytest.mark.parametrize("stars, expected_status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status, res.text
    expected = dict(rating)
    if expected_status == 200:
        assert res.json()["stars"] == stars
        expected["stars"] = stars
    else:
        assert res.json() == {"error": STARS_ERROR}
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == expected
