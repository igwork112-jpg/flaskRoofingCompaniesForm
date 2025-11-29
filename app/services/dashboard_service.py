"""Dashboard service for statistics and reporting."""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import func
from app.extensions import db
from app.models import Lead, LeadProcessingLog


class DashboardService:
    """Service for dashboard statistics and reporting."""
    
    @staticmethod
    def get_company_stats(company_id: int, filters: Optional[Dict] = None) -> Dict:
        """
        Get statistics for a company's leads.
        
        Args:
            company_id: The company ID
            filters: Optional filters (start_date, end_date)
            
        Returns:
            Dictionary with statistics
        """
        # Base query
        query = db.session.query(LeadProcessingLog).filter_by(company_id=company_id)
        
        # Apply date filters if provided
        if filters:
            if 'start_date' in filters:
                query = query.filter(LeadProcessingLog.created_at >= filters['start_date'])
            if 'end_date' in filters:
                query = query.filter(LeadProcessingLog.created_at <= filters['end_date'])
        
        # Get total count
        total_leads = query.count()
        
        # Get counts by status
        status_counts = db.session.query(
            LeadProcessingLog.status,
            func.count(LeadProcessingLog.id)
        ).filter_by(company_id=company_id)
        
        if filters:
            if 'start_date' in filters:
                status_counts = status_counts.filter(LeadProcessingLog.created_at >= filters['start_date'])
            if 'end_date' in filters:
                status_counts = status_counts.filter(LeadProcessingLog.created_at <= filters['end_date'])
        
        status_counts = status_counts.group_by(LeadProcessingLog.status).all()
        
        # Convert to dictionary
        counts_by_status = {
            'pending': 0,
            'processing': 0,
            'success': 0,
            'failed': 0
        }
        
        for status, count in status_counts:
            counts_by_status[status] = count
        
        # Calculate success rate
        processed_count = counts_by_status['success'] + counts_by_status['failed']
        success_rate = 0.0
        if processed_count > 0:
            success_rate = (counts_by_status['success'] / processed_count) * 100
        
        # Get failed leads with errors
        failed_leads = DashboardService.get_failed_leads(company_id, filters)
        
        return {
            'total_leads': total_leads,
            'counts_by_status': counts_by_status,
            'success_rate': round(success_rate, 2),
            'failed_leads': failed_leads
        }
    
    @staticmethod
    def get_failed_leads(company_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Get failed leads with error messages.
        
        Args:
            company_id: The company ID
            filters: Optional filters (start_date, end_date)
            
        Returns:
            List of failed lead dictionaries
        """
        query = db.session.query(LeadProcessingLog, Lead).join(
            Lead, LeadProcessingLog.lead_id == Lead.id
        ).filter(
            LeadProcessingLog.company_id == company_id,
            LeadProcessingLog.status == 'failed'
        )
        
        # Apply date filters if provided
        if filters:
            if 'start_date' in filters:
                query = query.filter(LeadProcessingLog.created_at >= filters['start_date'])
            if 'end_date' in filters:
                query = query.filter(LeadProcessingLog.created_at <= filters['end_date'])
        
        results = query.order_by(LeadProcessingLog.updated_at.desc()).limit(50).all()
        
        failed_leads = []
        for log, lead in results:
            failed_leads.append({
                'lead_id': lead.id,
                'lead_name': lead.name,
                'lead_phone': lead.phone,
                'error_message': log.error_message,
                'attempt_count': log.attempt_count,
                'failed_at': log.updated_at.isoformat() if log.updated_at else None
            })
        
        return failed_leads
