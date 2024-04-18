import pytest
# from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app


@pytest.fixture()
def client():
    client = TestClient(app)
    yield client


# @pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}


# @pytest.mark.asyncio
async def test_read_results(client):
    response = await client.get("/results")
    assert response.status_code == 200
    assert response.json() == []


# @pytest.mark.asyncio
async def test_classify_input(client):
    client.__enter__()

    test_message = "Love this beautiful country"
    response = await client.post(f"/classify/{test_message}")

    result_data = response.json()
    assert 'sentiment' in result_data
    sentiment = result_data['sentiment']
    assert type(sentiment) in (str, int)  # В зависимости от ожидаемого типа данных

    # Проверяем, что результат добавлен в базу данных
    response = client.get("/results")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]['message'] == test_message
    assert results[0]['sentiment'] == sentiment

    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}

    client.__exit__(None, None, None)
