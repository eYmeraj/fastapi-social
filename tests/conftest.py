import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
DATABAE_USERNAME = settings.database_username
DATABASE_PASSWORD = settings.database_password
DATABASE_HOSTNAME = settings.database_hostname
PORT_NUMBER = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABAE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}/{DATABASE_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TetsingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TetsingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email": "user@example.com",
                 "password": "password123"}
    res = client.post("/users/", json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def test_user_second(client):
    user_data = {"email": "user_second@example.com",
                 "password": "password123"}
    res = client.post("/users/", json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_posts(test_user, session):
    post_data = [
        {"title": "jjjj", "content": "gshs", "user_id": test_user["id"]},
        {"title": "jjsaa cajj", "content": "gsffashs", "user_id": test_user["id"]},
        {"title": "jefb5tjjj", "content": "sahjkshs", "user_id": test_user["id"]},
    ]

    post_data = list(map(lambda x: models.Post(**x), post_data))

    session.add_all(post_data)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture()
def test_posts_second(test_user_second, session):
    post_data = [
        {"title": "jjjj", "content": "gshs", "user_id": test_user_second["id"]},
        {"title": "jjsaa cajj", "content": "gsffashs", "user_id": test_user_second["id"]},
        {"title": "jefb5tjjj", "content": "sahjkshs", "user_id": test_user_second["id"]},
    ]

    post_data = list(map(lambda x: models.Post(**x), post_data))

    session.add_all(post_data)
    session.commit()
    posts = session.query(models.Post).all()
    return posts