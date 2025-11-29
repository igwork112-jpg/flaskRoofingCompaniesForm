"""Dashboard API endpoints."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.dashboard_service import DashboardService
from app.services.company_service import CompanyService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/<int:company_id>', methods=['GET'])
def get_dashboard(company_id: int):
    """
    Get dashboard view for a company.
    
    Query parameters:
    - start_date: Filter by start date (ISO format)
    - end_date: Filter by end date (ISO format)
    
    Returns:
        HTML dashboard (for now, returns JSON)
    """
    # Verify company exists
    company = CompanyService.get_company(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    # Parse filters
    filters = {}
    if request.args.get('start_date'):
        try:
            filters['start_date'] = datetime.fromisoformat(request.args.get('start_date'))
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
    
    if request.args.get('end_date'):
        try:
            filters['end_date'] = datetime.fromisoformat(request.args.get('end_date'))
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
    
    # Get statistics
    stats = DashboardService.get_company_stats(company_id, filters if filters else None)
    
    return jsonify({
        'company': company.to_dict(),
        'statistics': stats
    }), 200


@dashboard_bp.route('/api/<int:company_id>/stats', methods=['GET'])
def get_dashboard_stats(company_id: int):
    """
    Get dashboard statistics as JSON.
    
    Query parameters:
    - start_date: Filter by start date (ISO format)
    - end_date: Filter by end date (ISO format)
    
    Returns:
        JSON with statistics
    """
    # Verify company exists
    company = CompanyService.get_company(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    # Parse filters
    filters = {}
    if request.args.get('start_date'):
        try:
            filters['start_date'] = datetime.fromisoformat(request.args.get('start_date'))
        except ValueError:
            return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
    
    if request.args.get('end_date'):
        try:
            filters['end_date'] = datetime.fromisoformat(request.args.get('end_date'))
        except ValueError:
            return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
    
    # Get statistics
    stats = DashboardService.get_company_stats(company_id, filters if filters else None)
    
    return jsonify(stats), 200
