FROM python:3.11-slim

# Запрещаем Python создавать .pyc файлы и включаем буферизацию вывода (для удобного чтения логов)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только requirements, чтобы использовать кэш слоев Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]