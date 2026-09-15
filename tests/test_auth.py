import sys

sys.path.append(
    "c:/Users/hydro/OneDrive/Program Files/SentinelVaultRefactor/sentinel-vault-backend/src"
)

import pytest
from database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import StaticPool

from models import User


@pytest.fixture
def test_db():

    test_engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker[Session](bind=test_engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_user_registration_success(client):
    payload = {
        "username": "testuser",
        "email": "test@email.com",
        "password": "SecurePassword123!"
    }
    response = client.post("/api/register", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "User successfully registered!"


def test_login_invalid_password(client):
    payload = {"username": "testuser", "password": "WrongPassword"}
    response = client.post("/api/login", json=payload)
    assert response.status_code == 401
