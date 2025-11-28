"""Flask application factory."""
import os
from flask import Flask
from config import config
from app.extensions import db, migrate


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they're registered with SQLAlchemy
    from app.models import CompanyProfile, Lead, LeadProcessingLog
    
    # Register blueprints
    from app.api.web import web_bp
    from app.api.company import company_bp
    from app.api.leads import leads_bp
    from app.api.bulk import bulk_bp
    from app.api.dashboard import dashboard_bp
    from app.api.health import health_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(leads_bp)
    app.register_blueprint(bulk_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(health_bp)
    
    # Create tables if they don't exist (for development)
    with app.app_context():
        db.create_all()
    
    return app
