"""Bulk API endpoints."""
from flask import Blueprint, request, jsonify
from app.auth import require_api_key
from app.services.lead_service import LeadService
from app.services.validation import validate_lead_data

bulk_bp = Blueprint('bulk', __name__, url_prefix='/api')


@bulk_bp.route('/leads/bulk', methods=['POST'])
@require_api_key
def bulk_upload():
    """
    Bulk upload leads via API.
    
    Requires X-API-Key header for authentication.
    
    Expected JSON payload:
    {
        "leads": [
            {
                "name": "John Doe",
                "phone": "+1-555-1234",
                "notes": "Interested in roof repair",
                "company_id": 1
            },
            ...
        ]
    }
    
    Returns:
        JSON response with counts of successful and failed uploads
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    if 'leads' not in data or not isinstance(data['leads'], list):
        return jsonify({'error': 'Request must contain a "leads" array'}), 400
    
    if not data['leads']:
        return jsonify({'error': 'Leads array cannot be empty'}), 400
    
    # Validate all leads
    valid_leads = []
    invalid_leads = []
    
    for idx, lead_data in enumerate(data['leads']):
        validation_result = validate_lead_data(lead_data)
        
        if validation_result.is_valid:
            valid_leads.append(lead_data)
        else:
            invalid_leads.append({
                'index': idx,
                'data': lead_data,
                'errors': validation_result.errors
            })
    
    # Create and enqueue valid leads
    if valid_leads:
        enqueue_results = LeadService.create_and_enqueue_leads(valid_leads)
    else:
        enqueue_results = {
            'created': 0,
            'enqueued': 0,
            'failed': 0,
            'job_ids': []
        }
    
    return jsonify({
        'message': 'Bulk upload processed',
        'summary': {
            'total_submitted': len(data['leads']),
            'valid': len(valid_leads),
            'invalid': len(invalid_leads),
            'created': enqueue_results['created'],
            'enqueued': enqueue_results['enqueued'],
            'failed': enqueue_results['failed']
        },
        'invalid_leads': invalid_leads,
        'job_ids': enqueue_results['job_ids']
    }), 200
