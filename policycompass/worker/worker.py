import sys
sys.path.append('/app/backend')
import os
from rq import Worker, Queue, Connection
from redis import Redis

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(['comparison'])
        worker.work()
