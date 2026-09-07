import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

from app.main import app
from db.base import Base
from db.session import get_db
from models.user import User

env = dotenv_values(".env")
TEST_DATABASE_URL = env["TEST_DATABASE_URL"]
assert TEST_DATABASE_URL is not None, "TEST_DATABASE_URL not set in .env"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture()
def auth_headers(client):
    client.post('/auth/signup', json={'email': 'user@example.com', 'password': 'testpass123'})
    login = client.post('/auth/login', json={'email': 'user@example.com', 'password': 'testpass123'})
    token = login.json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture()
def admin_auth_headers(client, db_session):
    client.post('/auth/signup', json={'email': 'admin@example.com', 'password': 'testpass123'})
    user = db_session.query(User).filter(User.email == 'admin@example.com').first()
    user.is_admin = True
    db_session.commit()
    login = client.post('/auth/login', json={'email': 'admin@example.com', 'password': 'testpass123'})
    token = login.json()['access_token']
    return {'Authorization': f'Bearer {token}'}