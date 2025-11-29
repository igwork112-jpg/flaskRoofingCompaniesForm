"""Company profile model."""
from datetime import datetime
from app.extensions import db


class CompanyProfile(db.Model):
    """Model for roofing company profiles."""
    
    __tablename__ = 'company_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_phone = db.Column(db.String(20), nullable=False)
    owner_email = db.Column(db.String(100), nullable=False, unique=True)
    ghl_location_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leads = db.relationship('Lead', backref='company', lazy=True, cascade='all, delete-orphan')
    logs = db.relationship('LeadProcessingLog', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CompanyProfile {self.company_name}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'owner_name': self.owner_name,
            'owner_phone': self.owner_phone,
            'owner_email': self.owner_email,
            'ghl_location_id': self.ghl_location_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
