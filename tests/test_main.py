import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_index():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
            assert response.status_code == 200
            assert response.json() == {"index": "classification app working"}

            message = "Love this beautiful country"
            response = await ac.post(f"/classify/{message}")
            assert response.status_code == 200
            result_data =  response.json()

            assert 'sentiment' in result_data
            sentiment = result_data['sentiment']

            response = await ac.get("/results")
            assert response.status_code == 200
            results = response.json()
            assert len(results) == 1
            assert results[0]['message'] == message
            assert results[0]['sentiment'] == sentiment