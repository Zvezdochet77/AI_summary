import os
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@db:5432/summarizer_db"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/" 

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import asyncio
import pytest
import pytest_asyncio

from main import app 
@pytest.fixture(scope="session")
def event_loop():
    """Создает единственный event loop на всю тестовую сессию."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()