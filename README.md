# 🤖 AI Document Summarizer

An asynchronous, full-stack microservice application designed to process and summarize document contents using FastAPI, PostgreSQL, RabbitMQ, and Ollama (Local LLM).

## ✨ Features

- **Asynchronous Task Queue:** Long-running LLM summarization tasks are offloaded to RabbitMQ and processed in the background by dedicated workers.
- **Local LLM Integration:** Powered by Ollama (`llama3.2`) for private and fast document summarization without third-party API dependencies.
- **Multi-Format Document Upload:** Supports text parsing for `.txt`, `.pdf`, and `.docx` files via `python-multipart`, `PyPDF2`, and `python-docx`.
- **Real-Time UI Status Updates:** Modern, responsive frontend built with Tailwind CSS and Jinja2 templates, featuring automatic status polling (`pending` ⏳ ➔ `processing` ⚙️ ➔ `completed` ✅).
- **Containerized Architecture:** Fully dockerized setup managed with Docker Compose for seamless development and deployment.

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL + Async SQLAlchemy (`asyncpg`)
- **Message Broker:** RabbitMQ (`aio-pika`)
- **Background Worker:** Custom Python Async Worker
- **AI / LLM Service:** Ollama (`llama3.2:1b`)
- **Frontend:** HTML5, Tailwind CSS (via CDN), JavaScript (Fetch API / Polling), Jinja2 Templates
- **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```text
.
├── docker-compose.yml       # Docker Compose setup for all services
├── Dockerfile               # Base Dockerfile for Web API and Worker
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables configuration
├── main.py                  # FastAPI application (endpoints & Jinja2 setup)
├── worker.py                # Asynchronous RabbitMQ consumer & Ollama client
├── models.py                # SQLAlchemy ORM models
├── database.py              # Database session & engine connection
├── schemas.py               # Pydantic models (DTOs)
└── templates/
    └── index.html           # Frontend UI template