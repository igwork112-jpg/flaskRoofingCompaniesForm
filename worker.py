"""RQ worker startup script."""
import os
import sys
import redis
from rq import Worker, Queue, Connection
from app.app import create_app

# Create Flask app to get configuration
app = create_app()

def start_worker():
    """Start RQ worker."""
    with app.app_context():
        redis_url = app.config['REDIS_URL']
        queue_name = app.config['RQ_QUEUE_NAME']
        
        # Connect to Redis
        redis_conn = redis.from_url(redis_url)
        
        # Create queue
        queue = Queue(queue_name, connection=redis_conn)
        
        print(f"Starting worker for queue: {queue_name}")
        print(f"Redis URL: {redis_url}")
        
        # Start worker
        with Connection(redis_conn):
            worker = Worker([queue])
            worker.work()


if __name__ == '__main__':
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\nWorker stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Worker error: {str(e)}")
        sys.exit(1)
