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

async def test_create_document():
    """Тест успешного создания документа."""
    payload = {
        "title": "Название тестового документа", 
        "content": "Содержимое тестового документа" 
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/") as ac:
        response = await ac.post("/documents/", json = payload)
    assert response.status_code == 201
    data = response.json()
    assert payload["title"] == data["title"]
    assert data ["status"] == "pending"
    assert "id" in data

async def test_create_error_document():
    """Тест ошибок создания документа."""
    payload = {
        "title": "12", 
        "content": "12345" 
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/") as ac:
        response = await ac.post("/documents/", json = payload)
    assert response.status_code == 422


    
