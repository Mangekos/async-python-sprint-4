from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ping_db():
    response = client.get('/status/ping')
    assert response.status_code == 200