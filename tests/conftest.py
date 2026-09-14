import os
os.environ["DATABASE_URL"] = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:postgres@localhost:5432/summarizer_test_db"
)
os.environ["RABBITMQ_URL"] = os.getenv(
    "RABBITMQ_URL", 
    "amqp://guest:guest@localhost:5672/"
) 

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import asyncio
import pytest
import pytest_asyncio

from main import app
from database import engine, Base 
@pytest.fixture(scope="session")
def event_loop():
    """Создает единственный event loop на всю тестовую сессию."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Автоматически создает таблицы перед тестами и удаляет их после."""
    async with engine.begin() as conn:
       
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
