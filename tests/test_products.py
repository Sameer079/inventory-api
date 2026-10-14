import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/").json() == {"status": "ok"}


def test_product_crud(client):
    payload = {"name": "USB-C Cable", "sku": "CAB-001", "price": 9.99, "quantity": 40}
    created = client.post("/products", json=payload)
    assert created.status_code == 201
    pid = created.json()["id"]

    assert client.get(f"/products/{pid}").json()["sku"] == "CAB-001"

    updated = client.put(f"/products/{pid}", json={"quantity": 25})
    assert updated.json()["quantity"] == 25
    assert updated.json()["name"] == "USB-C Cable"

    assert client.delete(f"/products/{pid}").status_code == 204
    assert client.get(f"/products/{pid}").status_code == 404


def test_duplicate_sku_rejected(client):
    payload = {"name": "A", "sku": "X-1", "price": 1}
    assert client.post("/products", json=payload).status_code == 201
    assert client.post("/products", json=payload).status_code == 409


def test_validation_rejects_negative_price(client):
    r = client.post("/products", json={"name": "A", "sku": "X-2", "price": -5})
    assert r.status_code == 422


def test_search_and_category_filter(client):
    cat = client.post("/categories", json={"name": "Cables"}).json()
    client.post("/products", json={"name": "HDMI Cable", "sku": "H-1", "price": 5, "category_id": cat["id"]})
    client.post("/products", json={"name": "Mouse", "sku": "M-1", "price": 15})

    assert len(client.get("/products", params={"q": "hdmi"}).json()) == 1
    assert len(client.get("/products", params={"category_id": cat["id"]}).json()) == 1
    assert len(client.get("/products").json()) == 2
