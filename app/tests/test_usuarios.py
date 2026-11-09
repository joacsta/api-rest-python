import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_health():
    r = client.get("/")
    assert r.status_code == 200


def test_criar_usuario():
    r = client.post("/usuarios/", json={"nome": "Ana", "email": "ana@example.com"})
    assert r.status_code == 201
    assert r.json()["nome"] == "Ana"


def test_email_duplicado():
    client.post("usuarios/", json={"nome": "Ana", "email": "ana@example.com"})
    r = client.post("usuarios/", json={"nome": "Ana", "email": "ana@example.com"})
    assert r.status_code == 400


def test_buscar_usuario_inexistente():
    r = client.get("/usuario/999")
    assert r.status_code == 404
