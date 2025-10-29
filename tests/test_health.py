from fastapi.testclient import TestClient
from api.main import app

def test_health_ok():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_version_ok():
    c = TestClient(app)
    r = c.get("/version")
    body = r.json()
    assert r.status_code == 200 and "version" in body and body["name"].startswith("allO")
