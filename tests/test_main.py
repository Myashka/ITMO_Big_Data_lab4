from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}

def test_classify_endpoint(mocker):
    client.__enter__()

    mock_get_db = mocker.patch('main.get_db', return_value=AsyncMock())

    message = {"message": "What a lovely day"}
    response = client.post("/classify", json=message)
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}
    
    assert mock_get_db.called
    client.__exit__(None, None, None)