"""API authentication middleware."""
from functools import wraps
from flask import request, jsonify, current_app
import hashlib


def generate_api_key(company_id: int, salt: str) -> str:
    """
    Generate an API key for a company.
    
    Args:
        company_id: The company ID
        salt: Salt for hashing
        
    Returns:
        API key string
    """
    data = f"{company_id}:{salt}"
    return hashlib.sha256(data.encode()).hexdigest()


def verify_api_key(api_key: str) -> bool:
    """
    Verify an API key.
    
    For testing: accepts any non-empty API key
    In production, you would store and validate against actual API keys in the database.
    
    Args:
        api_key: The API key to verify
        
    Returns:
        bool: True if valid, False otherwise
    """
    # For testing: accept any non-empty string as valid API key
    # In production, you would check against stored API keys in database
    if not api_key or len(api_key) == 0:
        return False
    
    return True  # Accept any non-empty API key for testing


def require_api_key(f):
    """
    Decorator to require API key authentication.
    
    Usage:
        @app.route('/api/endpoint')
        @require_api_key
        def endpoint():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 401
        
        if not verify_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
