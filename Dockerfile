FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y build-essential

# Çalışma dizini
WORKDIR /app

# Requirements kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm projeyi kopyala
COPY . .

# Port
EXPOSE 8000

# Uvicorn ile FastAPI çalıştır
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
