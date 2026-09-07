import os
os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@db:5432/summarizer_db"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/" 

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app 