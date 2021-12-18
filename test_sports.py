from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Sever Up!"}


def test_read_sport():
    response = client.get("/sports/1")
    assert response.status_code == 200


def test_read_sport_all():
    response = client.get("/sports/")
    assert response.status_code == 200


def test_update_sport():
    response = client.put("/sports/1",
                          json={"name": "Foo Updated",
                                        "active": True,
                                        "slug": "foot"})
    assert response.status_code == 200


def test_create_sport():
    response = client.post("/sports/",
                          json={"name": "Foo",
                                        "active": True})
    assert response.status_code == 200


def test_create_event():
    response = client.post("/sports/",
                          json={"name": "Foo",
                                "active": True,
                                "slug": "foot"})
    assert response.status_code == 200
