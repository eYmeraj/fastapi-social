import pytest

from app import schemas

def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")
    def validate_post(post):
        return schemas.PostOut(**post)
        
    _ = list(map(validate_post, res.json())) # will error if not right format

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorised_get_one_post_not_exists(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{800000}")
    assert res.status_code == 404

def test_authorised_get_one_post_not_exists(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("title1", "content1", True),
    ("title1", "content1", False),
    ("title2", "content2", True),
    ("title3", "content", None),
])
def test_authorised_create_post(authorised_client, test_user, title, content, published):
    req_json = {
            "title": title,
            "content": content,
            "published": published
    }
    if not req_json["published"]:
        del req_json["published"]

    res = authorised_client.post("/posts/", json= req_json)
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    if published:
        assert created_post.published == published
    else:
        assert created_post.published == True

def test_authorised_delete_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_unauthorused_create_post(client, test_user):
    req_json = {"title": "some title", "content": "some content"}
    res = client.post("/posts/", json = req_json)
    assert res.status_code == 401

def test_unauthorused_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_not_owned(authorised_client, test_user, test_user_second, test_posts_second):
    res = authorised_client.delete(f"/posts/{test_posts_second[0].id}")
    assert res.status_code == 403

def test_update_post(authorised_client, test_user, test_posts):
    req_json = {
        "title": "new_title",
        "content": "new content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(f"/posts/{req_json['id']}", json = req_json)
    assert res.status_code == 200

# TODO:
#  Add more tests
