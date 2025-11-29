"""Lead processing log model."""
from datetime import datetime
from app.extensions import db


class LeadProcessingLog(db.Model):
    """Model for tracking lead processing status."""
    
    __tablename__ = 'lead_processing_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profiles.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # pending, processing, success, failed
    worker_id = db.Column(db.String(50), nullable=True)
    ghl_contact_id = db.Column(db.String(100), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    attempt_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        db.Index('idx_logs_company_status', 'company_id', 'status'),
        db.Index('idx_logs_status', 'status'),
    )
    
    def __repr__(self):
        return f'<LeadProcessingLog lead_id={self.lead_id} status={self.status}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'company_id': self.company_id,
            'status': self.status,
            'worker_id': self.worker_id,
            'ghl_contact_id': self.ghl_contact_id,
            'error_message': self.error_message,
            'attempt_count': self.attempt_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
