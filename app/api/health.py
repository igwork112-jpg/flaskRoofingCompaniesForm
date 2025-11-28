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
    if check_redis_health():
        health_status['checks']['redis'] = 'healthy'
    else:
        health_status['checks']['redis'] = 'unavailable (optional for testing)'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return jsonify(health_status), status_code
