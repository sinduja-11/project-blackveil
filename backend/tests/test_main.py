
from fastapi.testclient import TestClient

from app.main import app


# Create a test client
client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to PROJECT BLACKVEIL",
        "status": "running"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "PROJECT BLACKVEIL"
    assert data["status"] == "healthy"
    assert data["environment"] == "development"
