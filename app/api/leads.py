"""Lead API endpoints."""
from flask import Blueprint, request, jsonify
from app.services.lead_service import LeadService
from app.services.logging_service import LoggingService

leads_bp = Blueprint('leads', __name__, url_prefix='/leads')


@leads_bp.route('/single', methods=['POST'])
def upload_single():
    """
    Upload a single lead.
    
    Expected JSON payload:
    {
        "name": "John Doe",
        "phone": "+1-555-1234",
        "notes": "Interested in roof repair",
        "company_id": 1
    }
    
    Returns:
        JSON response with job ID or error messages
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Create lead
    lead, errors = LeadService.create_lead(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Create log entry
    log = LoggingService.create_log(lead.id, lead.company_id)
    
    # Enqueue lead for processing
    try:
        job_id = LeadService.enqueue_lead(lead)
        
        return jsonify({
            'message': 'Lead uploaded successfully',
            'lead_id': lead.id,
            'job_id': job_id,
            'lead': lead.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to enqueue lead: {str(e)}'}), 500


@leads_bp.route('/csv', methods=['POST'])
def upload_csv():
    """
    Upload leads via CSV file.
    
    Expected form data:
    - file: CSV file with columns: name, phone, notes (optional)
    - company_id: Company ID for all leads
    
    Returns:
        JSON response with summary of uploaded leads
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    if 'company_id' not in request.form:
        return jsonify({'error': 'company_id is required'}), 400
    
    file = request.files['file']
    company_id = request.form['company_id']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    
    try:
        company_id = int(company_id)
    except ValueError:
        return jsonify({'error': 'company_id must be a valid integer'}), 400
    
    # Read file content
    try:
        file_content = file.read().decode('utf-8')
    except Exception as e:
        return jsonify({'error': f'Failed to read file: {str(e)}'}), 400
    
    # Parse CSV
    parse_results = LeadService.parse_csv(file_content, company_id)
    
    if 'error' in parse_results:
        return jsonify({'error': parse_results['error']}), 400
    
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
    
    return jsonify({
        'message': 'CSV processed successfully',
        'summary': {
            'total_rows': parse_results['total'],
            'valid_rows': len(parse_results['valid']),
            'invalid_rows': len(parse_results['invalid']),
            'leads_created': enqueue_results['created'],
            'leads_enqueued': enqueue_results['enqueued'],
            'leads_failed': enqueue_results['failed']
        },
        'invalid_rows': parse_results['invalid'],
        'job_ids': enqueue_results['job_ids']
    }), 200
