from fastapi.testclient import TestClient
from app import app
import urllib

client = TestClient(app)




def test_create_event():
    response = client.post("/events/",
                          json={"name": "Event 4",
                                "slug": "string",
                                "active": True,
                                "sport_id": 4,
                                "type": "Preplay",
                                "status": "Pending",
                                "scheduled_start": "2021-12-21 14:48:51.497000"
                                })
    assert response.status_code == 200


def test_update_event():
    response = client.put("/events/2",
                          json={"name": "Event Edited",
                                "slug": "string",
                                "active": True,
                                "sport_id": 2,
                                "type": "Inplay",
                                "status": "Started",
                                "scheduled_start": "2021-12-21 15:59:51.497000"
                                })
    assert response.status_code == 200


def test_read_event():
    response = client.get("/events/1")
    assert response.status_code == 200


def test_read_event_filter():
    response = client.get("/filters/events?regex=E%5B%5Eg%5D%2B&threshold=3&=/")
    assert response.status_code == 200


def test_read_event_filter_date():
    params = {'regex': 'E[^g]+',
              'start_dt': '2021-12-21 12:59:51.497000-03:00',
              'end_dt': '2021-12-21 12:59:51.497000-03:00'}
    params_string = urllib.parse.urlencode(params)
    response = client.get(f"/filters/events?{params_string}")
    assert response.status_code == 200


def test_read_event_regex_date():
    params = {'name': 'E[^g]+'}
    params_string = urllib.parse.urlencode(params)
    response = client.get(f"/regex/events?{params_string}")
    assert response.status_code == 200


def test_read_event_all():
    response = client.get("/events/")
    assert response.status_code == 200






