from fastapi.testclient import TestClient
from fastapi.responses import Response


from main import app

client = TestClient(app)


def test_add_short_link():
    response: Response = client.post(
        "/links/add",
        json={"full_link": "https://www.google.com", "creator": "test"},
    )
    assert response.status_code == 201


def test_get_links():
    response = client.get("/links")
    assert response.status_code == 200


def test_get_full_link_not_found():
    response = client.get("/links/get/999")
    assert response.status_code == 404


def test_get_full_link_with_crossings():
    response = client.get("/links/get/1", headers={"host": "example.com"})
    assert response.status_code == 200


def test_del_short_link():
    response = client.get("/links/del/1")
    assert response.status_code == 204


def test_get_full_link_removed():
    response = client.get("/links/get/1")
    assert response.status_code == 410


def test_get_status():
    response = client.get("/status/1")
    assert response.status_code == 200
