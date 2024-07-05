FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]