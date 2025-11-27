# Task Queue System (FastAPI + Redis + RQ)

## What is included
- FastAPI app that enqueues tasks to Redis via RQ
- Worker that consumes jobs from Redis and executes them
- Dockerfiles and docker-compose for local testing
- GitHub Actions CI workflow to run tests
- Simple pytest test

## Local setup (Docker)
1. Install Docker and Docker Compose.
2. Clone this repo.
3. From repo root run:
   ```bash
   docker-compose up --build
   ```
4. API will be on `http://localhost:8000`.
   - Enqueue:
     ```bash
     curl -X POST "http://localhost:8000/enqueue" -H "Content-Type: application/json" -d '{"payload": {"n": 3}}'
     ```
   - Check status/result:
     `GET /status/<job_id>` or `GET /result/<job_id>`

## Run without Docker (using local Python)
1. Create virtualenv and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start Redis (locally or use Docker):
   ```bash
   docker run -p 6379:6379 redis:7-alpine
   ```
3. Start web:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Start worker (in another terminal):
   ```bash
   REDIS_URL=redis://localhost:6379/0 rq worker default
   ```

## Deploy to Render (free)
### Overview
We'll use a hosted Redis (Upstash) and Render for web + worker.
1. Create a GitHub repo and push this project.
2. Create an Upstash Redis free instance and copy the Redis URL.
3. Create two Render services:
   - Web Service (Docker) using `Dockerfile`
   - Background Worker (Docker) using `Dockerfile.worker`
4. Set the environment variable `REDIS_URL` to the Upstash Redis URL in both services' settings.
5. Deploy; Render will build Docker images and start services.

### Detailed steps
1. **Create GitHub repo**
   - Make a new repo on GitHub (private or public).
   - Push this project:
     ```bash
     git init
     git add .
     git commit -m "initial commit"
     git branch -M main
     git remote add origin <YOUR_GITHUB_URL>
     git push -u origin main
     ```
2. **Create Upstash Redis**
   - Sign up at https://console.upstash.com
   - Create a Redis database (Free tier)
   - Copy the `REDIS_URL` (use the non-ssl or the ssl url depending on Render settings)
3. **Create Render services**
   - Connect your GitHub repo to Render.
   - Create a new Web Service:
     - Environment: Docker
     - Branch: main
     - Build command: (Render will use Dockerfile automatically)
     - Set `REDIS_URL` env var to Upstash URL
   - Create a new Background Worker:
     - Environment: Docker
     - Command: (use default Docker CMD)
     - Set `REDIS_URL` env var to same Upstash URL
4. **Deploy**
   - Trigger a deploy on Render (it builds images, runs containers).
   - Web service will expose a domain like `https://your-app.onrender.com`.
   - Use that domain with the `/enqueue` endpoint.

## GitHub Actions
- The provided workflow runs tests on push/PR.

## Notes & Tips
- Upstash provides an authenticated Redis URL; set it as `REDIS_URL`.
- Render background workers are suitable for RQ workers; set the worker service to use the worker Dockerfile.
- If you get SSL/connection issues with Upstash, try using the TLS/SSL form `rediss://` and ensure your Redis client supports SSL (Redis.from_url does).
