from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from main import app


@pytest.fixture
def mock_db_session(monkeypatch):
    mock_session = AsyncMock(spec=AsyncSession)
    monkeypatch.setattr("src.db.database.get_db", lambda: mock_session)
    return mock_session

@pytest.fixture
def client():
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"index": "classification app working"}


@pytest.mark.asyncio
async def test_read_results(client, mock_db_session):
    mock_result = AsyncMock()
    mock_db_session.execute.return_value = mock_result
    mock_result.scalars.all.return_value = []

    response = await client.get("/results")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_classify_input(client, mock_db_session):
    # client.__enter__()

    # app.state.preprocessor = AsyncMock(return_value="processed message")
    # app.state.classifier.predict = AsyncMock(return_value={"sentiment": "positive"})

    mock_db_session.add = AsyncMock()
    mock_db_session.commit = AsyncMock()

    message = "Love this beautiful country"
    response = await client.post(f"/classify/{message}")
    assert response.status_code == 200
    assert response.json() == {"sentiment": "positive"}

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

    # client.__exit__(None, None, None)
