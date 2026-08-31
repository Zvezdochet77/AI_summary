import asyncio
import json
import os
import logging
import httpx
import aio_pika
from sqlalchemy.future import select
from dotenv import load_dotenv

from database import async_session
from models import Document 

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("worker")

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
OLLAMA_BASE_URL = os.getenv ("OLLAMA_BASE_URL")
MODEL_NAME = "llama3.2:1b" 

async def generate_summary(text: str) -> str:
    prompt = f"Сделай краткий и понятный конспект следующего текста на русском языке:\n\n{text}"
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json = {
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False 
            }
        ) 
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() 

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        doc_id = data.get("document_id")
        logger.info(f"[RabbitMQ] Получена задача для документа ID: {doc_id}")
        async with async_session() as db:
            result = await db.execute (select(Document).where(Document.id == doc_id))
            doc = result.scalar_one_or_none()
            if not doc:
                logger.error(f"Документ {doc_id} не найден в БД")
                return
            try:
                doc.status = "processing"
                await db.commit()
                logger.info (f"[llama] Отправка текста документа ID: {doc_id}")
                summary = await generate_summary (doc.content)
                doc.summary = summary 
                doc.status = "completed"
                await db.commit()
                logger.info (f"[llama] Документ ID успешно обработан: {doc_id}")
            except Exception as e:
                logger.error (f"[llama] Ошибка при обработке документа ID: {doc_id}, {e}")
                doc.status = "failed"
                await db.commit()
async def main():
    logger.info("Подключение к RabbitMQ")
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("summarization_tasks", durable=True)
        logger.info (f"[worker] Сервис запущен и ждет заданий")
        await queue.consume(process_message)
        await asyncio.Future()
if __name__ == "__main__":
    asyncio.run(main()) 



                
                                     