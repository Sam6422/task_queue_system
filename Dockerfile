FROM python:3.11-slim

# set working folder
WORKDIR /app

# copy the whole repo into /app so that /app/app exists
COPY . /app

# install build tools, deps, then clean to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    apt-get purge -y --auto-remove gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# start uvicorn pointing to package app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
