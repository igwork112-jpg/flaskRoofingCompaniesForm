"""Lead model."""
from datetime import datetime
from app.extensions import db


class Lead(db.Model):
    """Model for leads."""
    
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    logs = db.relationship('LeadProcessingLog', backref='lead', lazy=True, cascade='all, delete-orphan')
    
    # Index for performance
    __table_args__ = (
        db.Index('idx_leads_company', 'company_id'),
    )
    
    def __repr__(self):
        return f'<Lead {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'phone': self.phone,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
