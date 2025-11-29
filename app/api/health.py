"""Health check endpoints."""
from flask import Blueprint, jsonify
from app.extensions import db
from app.queue import check_redis_health

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Checks:
    - Database connectivity
    - Redis connectivity (optional for testing)
    
    Returns:
        JSON with health status
    """
    health_status = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database
    try:
        db.session.execute(db.text('SELECT 1'))
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Redis (optional - won't fail health check if unavailable)
    redis_healthy = check_redis_health()
    if redis_healthy:
        health_status['checks']['redis'] = 'healthy'
        health_status['checks']['bulk_uploads'] = 'enabled'
    else:
        health_status['checks']['redis'] = 'unavailable'
        health_status['checks']['bulk_uploads'] = 'disabled'
        health_status['warnings'] = ['Bulk API uploads are disabled while Redis is unavailable']
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return jsonify(health_status), status_code


@health_bp.route('/health/redis', methods=['GET'])
def redis_health():
    """
    Redis-specific health check.
    
    Returns:
        JSON with Redis status and queue information
    """
    from app.queue import get_queue
    
    redis_status = {
        'redis': 'unknown',
        'queue': 'unknown',
        'bulk_uploads': 'disabled'
    }
    
    if check_redis_health():
        redis_status['redis'] = 'healthy'
        redis_status['bulk_uploads'] = 'enabled'
        
        try:
            queue = get_queue()
            redis_status['queue'] = 'healthy'
            redis_status['queue_name'] = queue.name
            redis_status['pending_jobs'] = len(queue)
        except Exception as e:
            redis_status['queue'] = f'error: {str(e)}'
        
        return jsonify(redis_status), 200
    else:
        redis_status['redis'] = 'unavailable'
        redis_status['message'] = 'Redis is not running. Bulk uploads are disabled.'
        return jsonify(redis_status), 503
