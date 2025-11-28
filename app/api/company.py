"""Company API endpoints."""
from flask import Blueprint, request, jsonify
from app.services.company_service import CompanyService

company_bp = Blueprint('company', __name__, url_prefix='/company')


@company_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new company profile.
    
    Expected JSON payload:
    {
        "company_name": "ABC Roofing",
        "owner_name": "John Doe",
        "owner_email": "john@abcroofing.com",
        "owner_phone": "+1-555-1234",
        "ghl_location_id": "abc123"
    }
    
    Returns:
        JSON response with company ID or error messages
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    company, errors = CompanyService.register_company(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    return jsonify({
        'message': 'Company registered successfully',
        'company_id': company.id,
        'company': company.to_dict()
    }), 201
