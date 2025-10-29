from fastapi.testclient import TestClient
from api.main import app

def test_post_ticket_valid():
    c = TestClient(app)
    res = c.post("/ticket", json={
        "title": "Bondrucker druckt nicht",
        "description": "Seit 12:10 kein Bon. Kasse meldet Offline.",
        "profile": "gastro",
        "priority": "high",
        "customer": "Cafe Example"
    })
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert body["ticket"]["title"] == "Bondrucker druckt nicht"
    assert "id" in body["ticket"]
