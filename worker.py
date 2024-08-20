import os
import redis
from rq import Queue, SimpleWorker
from dotenv import load_dotenv
import multiprocessing as mp
from rq.timeouts import TimerDeathPenalty
import sys

# Load environment variables
load_dotenv()

# Specify the queue to listen on
listen = ['my_custom_queue']

# Redis connection URL from environment variables
redis_url = os.getenv('REDIS_URL')
if not redis_url:
    print("REDIS_URL is not set in environment variables. Please check your .env file.")
    sys.exit(1)

# Create Redis connection
conn = redis.from_url(redis_url)

def start_worker():
    try:
        queues = [Queue(name, connection=conn) for name in listen]
        worker = SimpleWorker(queues, connection=conn)
        worker.death_penalty_class = TimerDeathPenalty
        worker.work()
    except Exception as e:
        print(f"Worker error: {e}")

if __name__ == '__main__':
    if os.name == 'nt':
        p = mp.Process(target=start_worker)
        p.start()
        p.join()
    else:
        start_worker()
