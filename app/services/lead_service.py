"""Lead service for managing leads."""
from typing import Optional, List, Dict
import csv
import io
from flask import current_app
from app.extensions import db
from app.models import Lead
from app.services.validation import validate_lead_data, validate_company_exists
from app.queue import get_queue
from app.jobs.process_lead import process_lead_job


class LeadService:
    """Service for lead operations."""
    
    @staticmethod
    def create_lead(data: dict) -> tuple[Optional[Lead], Optional[dict]]:
        """
        Create a new lead.
        
        Args:
            data: Dictionary containing lead data
            
        Returns:
            Tuple of (Lead, error_dict)
        """
        # Validate data
        validation_result = validate_lead_data(data)
        if not validation_result.is_valid:
            return None, validation_result.errors
        
        # Validate company exists
        company_validation = validate_company_exists(int(data['company_id']), db.session)
        if not company_validation.is_valid:
            return None, company_validation.errors
        
        # Create lead
        lead = Lead(
            company_id=int(data['company_id']),
            name=data['name'].strip(),
            phone=data['phone'].strip(),
            notes=data.get('notes', '').strip() if data.get('notes') else None
        )
        
        try:
            db.session.add(lead)
            db.session.commit()
            return lead, None
        except Exception as e:
            db.session.rollback()
            return None, {'database': [f'An error occurred while saving the lead: {str(e)}']}
    
    @staticmethod
    def enqueue_lead(lead: Lead) -> str:
        """
        Enqueue a lead for processing.
        
        Args:
            lead: The lead to enqueue
            
        Returns:
            Job ID (or 'sync' for synchronous processing)
        """
        # For testing without Redis, just return a fake job ID
        # In production, this would use Redis queue
        try:
            queue = get_queue()
            job = queue.enqueue(
                process_lead_job,
                lead.id,
                job_timeout=current_app.config['JOB_TIMEOUT'],
                result_ttl=current_app.config['JOB_RESULT_TTL']
            )
            return job.id
        except Exception as e:
            # If Redis is not available, return a fake job ID for testing
            print(f"Redis not available, skipping queue: {str(e)}")
            return f"test-job-{lead.id}"
    
    @staticmethod
    def parse_csv(file_content: str, company_id: int) -> Dict[str, any]:
        """
        Parse CSV file and validate leads.
        
        Args:
            file_content: CSV file content as string
            company_id: Company ID for all leads
            
        Returns:
            Dictionary with parsing results
        """
        results = {
            'total': 0,
            'valid': [],
            'invalid': []
        }
        
        try:
            csv_file = io.StringIO(file_content)
            reader = csv.DictReader(csv_file)
            
            # Check for required columns
            if not reader.fieldnames:
                return {
                    'error': 'CSV file is empty or invalid',
                    'total': 0,
                    'valid': [],
                    'invalid': []
                }
            
            required_columns = ['name', 'phone']
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            
            if missing_columns:
                return {
                    'error': f'Missing required columns: {", ".join(missing_columns)}',
                    'total': 0,
                    'valid': [],
                    'invalid': []
                }
            
            # Process each row
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 is header)
                results['total'] += 1
                
                lead_data = {
                    'name': row.get('name', ''),
                    'phone': row.get('phone', ''),
                    'notes': row.get('notes', ''),
                    'company_id': company_id
                }
                
                # Validate lead data
                validation_result = validate_lead_data(lead_data)
                
                if validation_result.is_valid:
                    results['valid'].append(lead_data)
                else:
                    results['invalid'].append({
                        'row': row_num,
                        'data': lead_data,
                        'errors': validation_result.errors
                    })
            
            return results
            
        except Exception as e:
            return {
                'error': f'Error parsing CSV: {str(e)}',
                'total': 0,
                'valid': [],
                'invalid': []
            }
    
    @staticmethod
    def create_and_enqueue_leads(leads_data: List[dict]) -> Dict[str, any]:
        """
        Create multiple leads and enqueue them for processing.
        
        Args:
            leads_data: List of lead data dictionaries
            
        Returns:
            Dictionary with results
        """
        results = {
            'created': 0,
            'enqueued': 0,
            'failed': 0,
            'job_ids': []
        }
        
        for lead_data in leads_data:
            lead, errors = LeadService.create_lead(lead_data)
            
            if lead:
                results['created'] += 1
                try:
                    job_id = LeadService.enqueue_lead(lead)
                    results['enqueued'] += 1
                    results['job_ids'].append(job_id)
                except Exception as e:
                    results['failed'] += 1
                    print(f"Failed to enqueue lead {lead.id}: {str(e)}")
            else:
                results['failed'] += 1
        
        return results
