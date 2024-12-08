FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

# Встановлюємо Python-залежності
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо файли проєкту
COPY . .

# Відкриваємо порт для FastAPI
EXPOSE 8000

# Запускаємо FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
