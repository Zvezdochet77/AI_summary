import pytest
from httpx import AsyncClient, ASGITransport
from main import app


pytestmark = pytest.mark.asyncio

async def test_read_index ():
    """Тест отдачи главной страницы HTML."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "AI Document Summarizer" in response.text

async def  test_get_documents ():
    """Тест отдачи списков документов."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/") as ac:
        response = await ac.get("/documents/")
    assert response.status_code == 200
    assert isinstance (response.json(), list)