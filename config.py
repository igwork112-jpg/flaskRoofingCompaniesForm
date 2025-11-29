import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///roofing_leads.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # GoHighLevel
    GHL_API_KEY = os.getenv('GHL_API_KEY', '')
    GHL_API_BASE_URL = os.getenv('GHL_API_BASE_URL', 'https://rest.gohighlevel.com/v1')
    
    # API Authentication
    API_KEY_SALT = os.getenv('API_KEY_SALT', 'default-salt-change-in-production')
    
    # Worker Configuration
    WORKER_COUNT = int(os.getenv('WORKER_COUNT', 4))
    
    # Application Settings
    MAX_CSV_SIZE_MB = int(os.getenv('MAX_CSV_SIZE_MB', 10))
    MAX_CONTENT_LENGTH = MAX_CSV_SIZE_MB * 1024 * 1024  # Convert to bytes
    
    # Queue Settings
    RQ_QUEUE_NAME = 'lead_processing'
    JOB_TIMEOUT = 300  # 5 minutes
    JOB_RESULT_TTL = 86400  # 24 hours
    
    # Retry Settings
    MAX_RETRIES = 3
    RETRY_DELAYS = [1, 2, 4]  # Exponential backoff in seconds


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    REDIS_URL = 'redis://localhost:6379/1'  # Use different Redis DB for testing


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
