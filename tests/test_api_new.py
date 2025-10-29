from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_post_ask_ok():
    res = client.post("/ask", json={"query": "VPN verbindet nicht", "profile": "it"})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data and "intent" in data
