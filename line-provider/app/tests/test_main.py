from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)


def test_get_all_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_event_success():
    response = client.get("/event/1")
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "1"
    assert "coefficient" in data


def test_get_single_event_not_found():
    response = client.get("/event/999")
    assert response.status_code == 404


def test_create_new_event():
    new_event = {
        "event_id": "999",
        "coefficient": 1.99,
        "deadline": int(time.time()) + 300,
        "state": 1
    }
    response = client.put("/event", json=new_event)
    assert response.status_code == 200

    get_response = client.get("/event/999")
    assert get_response.status_code == 200
    assert get_response.json()["coefficient"] == "1.99"
