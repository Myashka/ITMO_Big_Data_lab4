import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
            
def test_read_main(client):
    response =  client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}

def test_requests(client):
    message = "Love this beautiful country"
    response =  client.post(f"/classify/{message}")
    assert response.status_code == 200
    result_data =  response.json()

    assert 'sentiment' in result_data   
    sentiment = result_data['sentiment']

    response =  client.get("/results")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]['message'] == message
    assert results[0]['sentiment'] == sentiment