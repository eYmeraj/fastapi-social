from jose import jwt

from app import schemas
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "welcome to api!!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email": "user@example.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())

    assert res.status_code == 201
    assert new_user.email == "user@example.com"

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
# [can add a bunch to test differnt casese]    
# ])
def test_incorrect_login(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"], "password": "wrong_pass"})

    assert res.status_code == 403
    assert res.json()["detail"] == "invalid credentials"


