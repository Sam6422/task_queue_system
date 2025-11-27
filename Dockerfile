FROM python:3.11-slim

WORKDIR /app
COPY ./app /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential &&             pip install --upgrade pip &&             pip install -r /app/requirements.txt &&             apt-get purge -y --auto-remove gcc build-essential &&             rm -rf /var/lib/apt/lists/*

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
