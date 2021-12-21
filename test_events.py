from fastapi.testclient import TestClient
from app import app

client = TestClient(app)




def test_create_event():
    response = client.post("/events/",
                          json={"name": "string",
                                "slug": "string",
                                "active": True,
                                "sport_id": 1,
                                "type": "Preplay",
                                "status": "Pending",
                                "scheduled_start": "2021-12-21T15:59:51.497Z"
                                })
    assert response.status_code == 200


def test_update_event():
    response = client.put("/events/1",
                          json={"name": "Event Edited",
                                "slug": "string",
                                "active": True,
                                "sport_id": 1,
                                "type": "Inplay",
                                "status": "Started",
                                "scheduled_start": "2021-12-21T15:59:51.497Z"
                                })
    assert response.status_code == 200


def test_read_event():
    response = client.get("/events/1")
    assert response.status_code == 200


def test_read_event_all():
    response = client.get("/events/")
    assert response.status_code == 200





