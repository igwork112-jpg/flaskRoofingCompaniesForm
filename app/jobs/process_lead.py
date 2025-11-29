"""Background job for processing leads."""
import time
from app.extensions import db
from app.models import Lead, CompanyProfile, LeadProcessingLog
from app.services.ghl_service import GHLService
from app.services.logging_service import LoggingService


def process_lead_job(lead_id: int):
    """
    Process a lead by sending it to GoHighLevel.
    
    This function is executed by RQ workers in the background.
    
    Args:
        lead_id: The ID of the lead to process
    """
    import os
    worker_id = os.getpid()  # Use process ID as worker identifier
    
    # Fetch lead and company profile
    lead = db.session.query(Lead).filter_by(id=lead_id).first()
    if not lead:
        print(f"Lead {lead_id} not found")
        return
    
    company = db.session.query(CompanyProfile).filter_by(id=lead.company_id).first()
    if not company:
        print(f"Company {lead.company_id} not found for lead {lead_id}")
        return
    
    # Get or create log
    log = db.session.query(LeadProcessingLog).filter_by(lead_id=lead_id).first()
    if not log:
        log = LoggingService.create_log(lead_id, lead.company_id)
    
    # Update log to processing status
    LoggingService.update_log_status(
        log.id,
        'processing',
        worker_id=str(worker_id)
    )
    
    # Initialize GHL service
    ghl_service = GHLService()
    
    # Build payload
    payload = ghl_service.build_contact_payload(lead, company)
    
    # Attempt to send to GHL with retries
    max_retries = 3
    retry_delays = [1, 2, 4]  # Exponential backoff
    
    for attempt in range(max_retries):
        try:
            # Send to GHL
            response = ghl_service.create_contact(company.ghl_location_id, payload)
            
            # Success - update log
            LoggingService.update_log_status(
                log.id,
                'success',
                ghl_contact_id=response.get('contact', {}).get('id'),
                attempt_count=attempt + 1
            )
            print(f"Successfully processed lead {lead_id}")
            return
            
        except Exception as e:
            error_message = str(e)
            print(f"Attempt {attempt + 1} failed for lead {lead_id}: {error_message}")
            
            # If this was the last attempt, mark as failed
            if attempt == max_retries - 1:
                LoggingService.update_log_status(
                    log.id,
                    'failed',
                    error_message=error_message,
                    attempt_count=attempt + 1
                )
                print(f"Failed to process lead {lead_id} after {max_retries} attempts")
                return
            
            # Wait before retrying
            time.sleep(retry_delays[attempt])
            
            # Update attempt count
            log.attempt_count = attempt + 1
            db.session.commit()
