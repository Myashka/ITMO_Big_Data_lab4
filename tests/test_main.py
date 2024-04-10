from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}


def test_classify_endpoint():
    client.__enter__()

    message = "Love this beautiful country"
    response = client.get(f"/classify/{message}")
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}

    client.__exit__(None, None, None)