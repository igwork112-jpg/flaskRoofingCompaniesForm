"""Logging service for tracking lead processing."""
from typing import List, Optional, Dict
from datetime import datetime
from app.extensions import db
from app.models import LeadProcessingLog


class LoggingService:
    """Service for lead processing log operations."""
    
    @staticmethod
    def create_log(lead_id: int, company_id: int) -> LeadProcessingLog:
        """
        Create a new processing log with pending status.
        
        Args:
            lead_id: The lead ID
            company_id: The company ID
            
        Returns:
            LeadProcessingLog instance
        """
        log = LeadProcessingLog(
            lead_id=lead_id,
            company_id=company_id,
            status='pending',
            attempt_count=0
        )
        
        db.session.add(log)
        db.session.commit()
        
        return log
    
    @staticmethod
    def update_log_status(log_id: int, status: str, **kwargs) -> LeadProcessingLog:
        """
        Update log status and related fields.
        
        Args:
            log_id: The log ID
            status: New status (pending, processing, success, failed)
            **kwargs: Additional fields to update (worker_id, ghl_contact_id, error_message, attempt_count)
            
        Returns:
            Updated LeadProcessingLog instance
        """
        log = db.session.query(LeadProcessingLog).filter_by(id=log_id).first()
        
        if not log:
            raise ValueError(f"Log with id {log_id} not found")
        
        log.status = status
        log.updated_at = datetime.utcnow()
        
        # Update optional fields
        if 'worker_id' in kwargs:
            log.worker_id = kwargs['worker_id']
        
        if 'ghl_contact_id' in kwargs:
            log.ghl_contact_id = kwargs['ghl_contact_id']
        
        if 'error_message' in kwargs:
            log.error_message = kwargs['error_message']
        
        if 'attempt_count' in kwargs:
            log.attempt_count = kwargs['attempt_count']
        
        db.session.commit()
        
        return log
    
    @staticmethod
    def get_logs_by_company(company_id: int, filters: Optional[Dict] = None) -> List[LeadProcessingLog]:
        """
        Get logs for a company with optional filters.
        
        Args:
            company_id: The company ID
            filters: Optional dictionary with filter criteria
                - status: Filter by status
                - start_date: Filter by created_at >= start_date
                - end_date: Filter by created_at <= end_date
                
        Returns:
            List of LeadProcessingLog instances
        """
        query = db.session.query(LeadProcessingLog).filter_by(company_id=company_id)
        
        if filters:
            if 'status' in filters:
                query = query.filter_by(status=filters['status'])
            
            if 'start_date' in filters:
                query = query.filter(LeadProcessingLog.created_at >= filters['start_date'])
            
            if 'end_date' in filters:
                query = query.filter(LeadProcessingLog.created_at <= filters['end_date'])
        
        return query.order_by(LeadProcessingLog.created_at.desc()).all()
    
    @staticmethod
    def get_log_by_lead(lead_id: int) -> Optional[LeadProcessingLog]:
        """
        Get log for a specific lead.
        
        Args:
            lead_id: The lead ID
            
        Returns:
            LeadProcessingLog instance or None
        """
        return db.session.query(LeadProcessingLog).filter_by(lead_id=lead_id).first()
