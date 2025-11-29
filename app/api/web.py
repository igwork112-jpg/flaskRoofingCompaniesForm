"""Web UI routes for forms."""
from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models import CompanyProfile, Lead, LeadProcessingLog
from app.services.company_service import CompanyService
from app.services.lead_service import LeadService
from app.services.logging_service import LoggingService
from sqlalchemy import func

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def index():
    """Home page."""
    # Get stats
    total_companies = db.session.query(CompanyProfile).count()
    total_leads = db.session.query(Lead).count()
    
    stats = {
        'total_companies': total_companies,
        'total_leads': total_leads
    }
    
    return render_template('index.html', stats=stats)


@web_bp.route('/register-company', methods=['GET', 'POST'])
def register_company():
    """Company registration form."""
    if request.method == 'POST':
        # Get form data
        data = {
            'company_name': request.form.get('company_name'),
            'owner_name': request.form.get('owner_name'),
            'owner_email': request.form.get('owner_email'),
            'owner_phone': request.form.get('owner_phone'),
            'ghl_location_id': request.form.get('ghl_location_id')
        }
        
        # Register company
        company, errors = CompanyService.register_company(data)
        
        if errors:
            return render_template('register_company.html', 
                                 errors=errors, 
                                 form_data=data)
        
        return render_template('register_company.html', 
                             success=True, 
                             company_id=company.id,
                             form_data={})
    
    return render_template('register_company.html', form_data={})


@web_bp.route('/add-lead', methods=['GET', 'POST'])
def add_lead():
    """Add lead form - handles both single and CSV upload."""
    # Get all companies for dropdown
    companies = db.session.query(CompanyProfile).order_by(CompanyProfile.company_name).all()
    
    if request.method == 'POST':
        upload_type = request.form.get('upload_type', 'single')
        
        if upload_type == 'csv':
            # Handle CSV upload
            if 'file' not in request.files:
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error='No file uploaded',
                                     form_data={})
            
            file = request.files['file']
            company_id = request.form.get('company_id')
            
            if file.filename == '':
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error='No file selected',
                                     form_data={'company_id': company_id})
            
            if not file.filename.endswith('.csv'):
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error='File must be a CSV',
                                     form_data={'company_id': company_id})
            
            try:
                company_id = int(company_id)
            except (ValueError, TypeError):
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error='Invalid company selected',
                                     form_data={})
            
            # Read and parse CSV
            try:
                file_content = file.read().decode('utf-8')
            except Exception as e:
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error=f'Failed to read file: {str(e)}',
                                     form_data={'company_id': company_id})
            
            parse_results = LeadService.parse_csv(file_content, company_id)
            
            if 'error' in parse_results:
                return render_template('add_lead.html', 
                                     companies=companies,
                                     error=parse_results['error'],
                                     form_data={'company_id': company_id})
            
            # Create and enqueue valid leads
            if parse_results['valid']:
                enqueue_results = LeadService.create_and_enqueue_leads(parse_results['valid'])
            else:
                enqueue_results = {'created': 0, 'enqueued': 0, 'failed': 0}
            
            summary = {
                'total_rows': parse_results['total'],
                'valid_rows': len(parse_results['valid']),
                'invalid_rows': len(parse_results['invalid']),
                'leads_created': enqueue_results['created'],
                'leads_enqueued': enqueue_results['enqueued']
            }
            
            return render_template('add_lead.html', 
                                 companies=companies,
                                 success=True,
                                 success_message='CSV processed successfully!',
                                 summary=summary,
                                 form_data={})
        
        else:
            # Handle single lead
            data = {
                'company_id': request.form.get('company_id'),
                'name': request.form.get('name'),
                'phone': request.form.get('phone'),
                'notes': request.form.get('notes', '')
            }
            
            lead, errors = LeadService.create_lead(data)
            
            if errors:
                return render_template('add_lead.html', 
                                     companies=companies,
                                     errors=errors, 
                                     form_data=data)
            
            # Create log entry
            log = LoggingService.create_log(lead.id, lead.company_id)
            
            # Try to enqueue
            try:
                job_id = LeadService.enqueue_lead(lead)
            except Exception as e:
                print(f"Could not enqueue lead: {str(e)}")
            
            return render_template('add_lead.html', 
                                 companies=companies,
                                 success=True,
                                 success_message='Lead added successfully!',
                                 lead_id=lead.id,
                                 form_data={})
    
    return render_template('add_lead.html', companies=companies, form_data={})


@web_bp.route('/dashboard')
@web_bp.route('/companies')
def list_companies():
    """Dashboard - List all companies with stats."""
    # Get all companies
    companies = db.session.query(CompanyProfile).order_by(CompanyProfile.created_at.desc()).all()
    
    # Add metrics for each company
    for company in companies:
        # Total leads uploaded
        company.lead_count = db.session.query(Lead).filter_by(company_id=company.id).count()
        
        # Count by status
        status_counts = db.session.query(
            LeadProcessingLog.status,
            func.count(LeadProcessingLog.id)
        ).filter_by(company_id=company.id).group_by(LeadProcessingLog.status).all()
        
        company.pending_count = 0
        company.processing_count = 0
        company.success_count = 0
        company.failed_count = 0
        
        for status, count in status_counts:
            if status == 'pending':
                company.pending_count = count
            elif status == 'processing':
                company.processing_count = count
            elif status == 'success':
                company.success_count = count
            elif status == 'failed':
                company.failed_count = count
        
        # Reactivated leads (success status)
        # This represents leads that were successfully sent to GHL
        
        # Response rate (for now, calculate as success / total processed)
        total_processed = company.success_count + company.failed_count
        if total_processed > 0:
            company.response_rate = round((company.success_count / total_processed) * 100, 1)
        else:
            company.response_rate = 0
        
        # Appointments set (placeholder - would come from GHL webhook data)
        # For now, estimate as a percentage of successful leads
        company.appointments_set = round(company.success_count * 0.3)  # Assume 30% conversion
    
    return render_template('dashboard.html', companies=companies)


@web_bp.route('/upload-csv', methods=['GET', 'POST'])
def upload_csv():
    """CSV upload form."""
    # Get all companies for dropdown
    companies = db.session.query(CompanyProfile).order_by(CompanyProfile.company_name).all()
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error='No file uploaded',
                                 form_data={})
        
        file = request.files['file']
        company_id = request.form.get('company_id')
        
        if file.filename == '':
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error='No file selected',
                                 form_data={'company_id': company_id})
        
        if not file.filename.endswith('.csv'):
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error='File must be a CSV',
                                 form_data={'company_id': company_id})
        
        try:
            company_id = int(company_id)
        except (ValueError, TypeError):
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error='Invalid company selected',
                                 form_data={})
        
        # Read file content
        try:
            file_content = file.read().decode('utf-8')
        except Exception as e:
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error=f'Failed to read file: {str(e)}',
                                 form_data={'company_id': company_id})
        
        # Parse CSV
        parse_results = LeadService.parse_csv(file_content, company_id)
        
        if 'error' in parse_results:
            return render_template('upload_csv.html', 
                                 companies=companies,
                                 error=parse_results['error'],
                                 form_data={'company_id': company_id})
        
        # Create and enqueue valid leads
        if parse_results['valid']:
            enqueue_results = LeadService.create_and_enqueue_leads(parse_results['valid'])
        else:
            enqueue_results = {
                'created': 0,
                'enqueued': 0,
                'failed': 0,
                'job_ids': []
            }
        
        summary = {
            'total_rows': parse_results['total'],
            'valid_rows': len(parse_results['valid']),
            'invalid_rows': len(parse_results['invalid']),
            'leads_created': enqueue_results['created'],
            'leads_enqueued': enqueue_results['enqueued']
        }
        
        return render_template('upload_csv.html', 
                             companies=companies,
                             success=True,
                             summary=summary,
                             invalid_rows=parse_results['invalid'],
                             form_data={})
    
    return render_template('upload_csv.html', companies=companies, form_data={})


@web_bp.route('/download-sample-csv')
def download_sample_csv():
    """Download a sample CSV file."""
    from flask import make_response
    
    csv_content = """name,phone,notes
John Smith,+1-555-1111,Interested in new roof installation
Mary Johnson,+1-555-2222,Roof repair needed - leak in kitchen
Bob Williams,+1-555-3333,Request for free inspection
Sarah Davis,+1-555-4444,Looking for roof replacement quote
"""
    
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=sample_leads.csv'
    
    return response
