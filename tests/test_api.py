"""API tests with Playwright's request context (no browser), against the public JSONPlaceholder API."""
import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_get_single_post(api):
    response = api.get("/posts/1")
    assert response.status == 200
    body = response.json()
    assert body["id"] == 1
    assert {"userId", "id", "title", "body"} <= body.keys()


def test_list_posts_returns_100_items(api):
    response = api.get("/posts")
    assert response.status == 200
    assert len(response.json()) == 100


def test_filter_posts_by_user(api):
    response = api.get("/posts", params={"userId": 1})
    assert response.status == 200
    posts = response.json()
    assert posts, "expected at least one post for userId=1"
    assert all(post["userId"] == 1 for post in posts)


def test_create_post(api):
    payload = {"title": "qa portfolio", "body": "created by a test", "userId": 1}
    response = api.post("/posts", data=payload)
    assert response.status == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert "id" in body


def test_update_post(api):
    response = api.put("/posts/1", data={"id": 1, "title": "updated", "body": "x", "userId": 1})
    assert response.status == 200
    assert response.json()["title"] == "updated"


def test_delete_post(api):
    assert api.delete("/posts/1").status == 200


def test_missing_post_returns_404(api):
    assert api.get("/posts/99999").status == 404


def test_response_is_json(api):
    response = api.get("/posts/1")
    assert "application/json" in response.headers["content-type"]
