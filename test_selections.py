from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_selection():
    response = client.get("/selections/1")
    assert response.status_code == 200


def test_create_selection():
    response = client.post("/selections/",
                          json={"name": "string",
                              "slug": "string",
                              "active": True,
                              "event_id": 3,
                              "status": "Started",
                              "price": 0.1,
                              "outcome": "Win"})
    assert response.status_code == 200


def test_update_selection():
    response = client.put("/selections/1",
                          json={"name": "Selection Edited",
                              "slug": "Selection",
                              "active": True,
                              "event_id": 3,
                              "status": "Started",
                              "price": 0.1,
                              "outcome": "Win"
                            })
    assert response.status_code == 200


def test_read_selection_all():
    response = client.get("/selections/")
    assert response.status_code == 200