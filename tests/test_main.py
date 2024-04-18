import pytest
from httpx import AsyncClient

from main import app


@pytest.fixture
def client():
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}


@pytest.mark.asyncio
async def test_read_results(client):
    response = await client.get("/results")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_classify_input(client):
    client.__enter__()

    message = "Love this beautiful country"
    response = await client.post(f"/classify/{message}")
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}

    client.__exit__(None, None, None)
