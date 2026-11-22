from fastapi.testclient import TestClient
from cleanslate.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_profile_csv():
    response = client.post("/api/v1/profile",
        files={"file": ("sample.csv", b"name,age\nAlice,20\nBob,\n", "text/csv")})
    assert response.status_code == 200
    assert response.json()["profile"]["row_count"] == 2

def test_reject_unsupported_extension():
    response = client.post("/api/v1/profile",
        files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 400
