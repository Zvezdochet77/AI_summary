from contextlib import asynccontextmanager 
from fastapi import FastAPI, Depends, HTTPException, status, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import Base, engine, get_db
from models import Document
from schemas import DocumentCreate, DocumentResponse
import os
from dotenv import load_dotenv
import aio_pika
import json
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List


load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

templates = Jinja2Templates(directory= "templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    #код выполняемый при запуске
    #ассинхронный запуск 
    async with engine.begin () as con:
        await con.run_sync(Base.metadata.create_all)
    yield  
app = FastAPI (
    title= "AISummaryGen",
    version= "1.0.0",
    lifespan=lifespan
    )

@app.get ("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name ="index.html", request=request,context= {
        "title": "AI Summarizer"
    }) 

@app.post("/documents/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(doc_data: DocumentCreate, db: AsyncSession=Depends(get_db)):
    newdoc = Document(
        title = doc_data.title,
        content = doc_data.content,
        status = "pending"
    )
    db.add(newdoc) 
    await db.commit ()
    await db.refresh (newdoc)
    connecting = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connecting:
        channel = await connecting.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body = json.dumps({"document_id": newdoc.id}).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT 
            ),
          routing_key="summarization_tasks"     
        ) 


    return newdoc

@app.get("/documents/{doc_id}", response_model=DocumentResponse)
async def get_document (doc_id: int, db: AsyncSession=Depends (get_db)):
    result = await db.execute(select(Document).where (Document.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return doc 
       
@app.get ("/documents/", response_model= List [DocumentResponse])
async def get_documents (db: AsyncSession=Depends (get_db)):
    result = await db.execute(select(Document).order_by(Document.id.desc()))
    documents = result.scalars ().all()
    return documents  

@app.post ("/documents/upload/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_documents (file: UploadFile = File (...), db: AsyncSession = Depends (get_db)):
    content = await file.read()
    content = content.decode("utf-8")
    newdoc = Document(
        title = file.filename,
        content = content,
        status = "pending"
    )
    db.add (newdoc)
    await db.commit ()
    await db.refresh (newdoc)
    connecting = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connecting:
        channel = await connecting.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body = json.dumps({"document_id": newdoc.id}).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT 
            ),
            routing_key="summarization_tasks"     
        ) 


    return newdoc
    

    