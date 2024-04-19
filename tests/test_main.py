import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_app():
    with TestClient(app) as client:
        app.router.startup()
        yield client
        app.router.shutdown()
            
def test_read_main(test_app):
    response =  test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}

def test_requests(test_app):
    message = "Love this beautiful country"
    response =  test_app.post(f"/classify/{message}")
    assert response.status_code == 200
    result_data =  response.json()

    assert 'sentiment' in result_data   
    sentiment = result_data['sentiment']

    response =  test_app.get("/results")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]['message'] == message
    assert results[0]['sentiment'] == sentiment