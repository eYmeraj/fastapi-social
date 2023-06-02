import pytest

from app import models

@pytest.fixture()
def test_like(session, test_user, test_posts_second):
    new_like = models.Like(post_id= test_posts_second[0].id, user_id = test_user["id"])
    session.add(new_like)
    session.commit()


def test_like_on_post(authorised_client, test_user, test_posts_second):
    req_json = {"post_id": test_posts_second[0].id,
                "direction": 1}
    res = authorised_client.post("/likes/", json = req_json)
    assert res.status_code == 201

def test_like_on_liked_post(authorised_client, test_user, test_like, test_posts_second):
    req_json = {"post_id": test_posts_second[0].id,
                "direction": 1}
    res = authorised_client.post("/likes/", json = req_json)
    assert res.status_code == 409

def test_unlike_post(authorised_client, test_user, test_like, test_posts_second):
    req_json = {"post_id": test_posts_second[0].id,
                "direction": 0}
    res = authorised_client.post("/likes/", json = req_json)
    assert res.status_code == 201

def test_unlike_post_not_liked(authorised_client, test_user, test_posts_second):
    req_json = {"post_id": test_posts_second[0].id,
                "direction": 0}
    res = authorised_client.post("/likes/", json = req_json)
    assert res.status_code == 404

def test_unlike_post_not_found(authorised_client, test_user, test_posts_second):
    req_json = {"post_id": -99999,
                "direction": 0}
    res = authorised_client.post("/likes/", json = req_json)
    assert res.status_code == 404

def test_unauthanticated_like(client, test_user, test_like, test_posts_second):
    req_json = {"post_id": test_posts_second[0].id,
                "direction": 1}
    res = client.post("/likes/", json = req_json)
    assert res.status_code == 401