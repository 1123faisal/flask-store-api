import os
import sys

import redis
from dotenv import load_dotenv
from rq import Queue, SimpleWorker, Worker

load_dotenv()

QUEUES = ["emails"]


def main():
    conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    queues = [Queue(name, connection=conn) for name in QUEUES]

    # os.fork() isn't available on Windows, so the default forking Worker crashes there.
    worker_class = SimpleWorker if sys.platform == "win32" else Worker
    worker = worker_class(queues, connection=conn)
    worker.work()


if __name__ == "__main__":
    main()
