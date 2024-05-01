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

import time


def test_requests(test_app):
    message = "Love this beautiful country"
    # Отправляем сообщение на классификацию
    response = test_app.post(f"/classify/{message}")
    assert response.status_code == 200
    assert response.json() == {"status": "Message sent to Kafka"}

    time.sleep(5)

    # Получаем все результаты
    response = test_app.get("/results")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0

    last_result = results[-1]
    assert last_result['message'] == message

    response = test_app.get(f"/results/{last_result['id']}")
    assert response.status_code == 200
    result_data = response.json()
    assert result_data['message'] == message
    assert 'sentiment' in result_data

