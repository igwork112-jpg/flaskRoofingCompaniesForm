"""Redis queue configuration."""
import redis
from rq import Queue
from flask import current_app


def get_redis_connection():
    """
    Get Redis connection from app config.
    
    Returns:
        Redis connection instance
    """
    redis_url = current_app.config['REDIS_URL']
    return redis.from_url(redis_url)


def get_queue():
    """
    Get RQ queue instance.
    
    Returns:
        RQ Queue instance
    """
    redis_conn = get_redis_connection()
    queue_name = current_app.config['RQ_QUEUE_NAME']
    return Queue(queue_name, connection=redis_conn)


def check_redis_health():
    """
    Check if Redis is accessible.
    
    Returns:
        bool: True if Redis is healthy, False otherwise
    """
    try:
        redis_conn = get_redis_connection()
        redis_conn.ping()
        return True
    except Exception as e:
        print(f"Redis health check failed: {str(e)}")
        return False
