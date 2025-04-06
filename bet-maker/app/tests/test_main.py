from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_place_bet_success():
    payload = {
        "event_id": "1",
        "amount": 10.50
    }
    response = client.post("/bet", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "bet_id" in data


def test_place_bet_invalid_event():
    payload = {
        "event_id": "999999",
        "amount": 15.00
    }
    response = client.post("/bet", json=payload)
    assert response.status_code in [404, 400]


def test_get_bets():
    response = client.get("/bets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
