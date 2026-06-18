import asyncio
from rq import Queue
from redis import Redis
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_conn = Redis.from_url(redis_url)
queue = Queue("comparison", connection=redis_conn)

def run_comparison_job(comparison_id: str):
    from backend.comparison_worker import process_comparison
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_comparison(comparison_id))
