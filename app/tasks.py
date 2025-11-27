# app/tasks.py
import time
import random

def long_running_task(data: dict):
    """Example long-running task: pretend to process `data` and return a result."""
    total = 0
    n = int(data.get("n", 5))
    for i in range(n):
        time.sleep(1)
        total += i * random.random()
    result = {
        "input": data,
        "computed_total": total,
        "message": f"Processed {n} iterations"
    }
    return result
