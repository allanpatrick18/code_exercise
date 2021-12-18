from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_read_event():
    response = client.get("/events/1")
    assert response.status_code == 200


def test_create_event():
    response = client.post("/events/",
                          json={"name": "string",
                                  "slug": "string",
                                  "active": True,
                                  "sport_id": 1,
                                  "status": "Preplay"})
    assert response.status_code == 200


def test_update_event():
    response = client.put("/events/1",
                          json={"name": "Events edit",
                                  "slug": "string",
                                  "active": True,
                                  "sport_id": 1,
                                  "status": "Inplay"})
    assert response.status_code == 200


def test_read_event_all():
    response = client.get("/events/")
    assert response.status_code == 200


