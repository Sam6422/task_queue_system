# app/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from rq.job import Job
from typing import Optional
from app.tasks import long_running_task

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  # docker-compose default
redis_conn = Redis.from_url(REDIS_URL)
q = Queue("default", connection=redis_conn)

app = FastAPI(title="Task Queue API")

class EnqueueRequest(BaseModel):
    payload: dict
    delay_seconds: Optional[int] = 0

@app.post("/enqueue")
def enqueue_task(req: EnqueueRequest):
    job = q.enqueue(long_running_task, req.payload, job_timeout=60*10, delay=req.delay_seconds)
    return {"job_id": job.get_id(), "status": job.get_status()}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job.get_id(), "status": job.get_status(), "result": job.result}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.is_finished:
        return {"job_id": job.get_id(), "result": job.result}
    elif job.is_failed:
        return {"job_id": job.get_id(), "status": "failed", "exc_info": str(job.exc_info)}
    else:
        return {"job_id": job.get_id(), "status": job.get_status()}
