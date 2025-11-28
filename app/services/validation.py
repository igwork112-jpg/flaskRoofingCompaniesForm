"""Validation service for input data."""
import re
from typing import Dict, List, Optional


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool = True, errors: Optional[Dict[str, List[str]]] = None):
        self.is_valid = is_valid
        self.errors = errors or {}
    
    def add_error(self, field: str, message: str):
        """Add an error message for a field."""
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
        self.is_valid = False


def validate_name(name: str) -> ValidationResult:
    """
    Validate that a name is non-empty and not just whitespace.
    
    Args:
        name: The name to validate
        
    Returns:
        ValidationResult indicating if the name is valid
    """
    result = ValidationResult()
    
    if not name or not name.strip():
        result.add_error('name', 'Name cannot be empty or contain only whitespace')
    
    return result


def validate_email(email: str) -> ValidationResult:
    """
    Validate email format.
    
    Args:
        email: The email address to validate
        
    Returns:
        ValidationResult indicating if the email is valid
    """
    result = ValidationResult()
    
    if not email or not email.strip():
        result.add_error('email', 'Email cannot be empty')
        return result
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email.strip()):
        result.add_error('email', 'Invalid email format')
    
    return result


def validate_phone(phone: str) -> ValidationResult:
    """
    Validate phone format - should contain only digits and valid formatting characters.
    
    Args:
        phone: The phone number to validate
        
    Returns:
        ValidationResult indicating if the phone is valid
    """
    result = ValidationResult()
    
    if not phone or not phone.strip():
        result.add_error('phone', 'Phone cannot be empty')
        return result
    
    # Allow digits, spaces, parentheses, hyphens, plus signs
    phone_pattern = r'^[\d\s\(\)\-\+]+$'
    
    if not re.match(phone_pattern, phone.strip()):
        result.add_error('phone', 'Phone can only contain digits and valid formatting characters (spaces, parentheses, hyphens, plus signs)')
    
    # Check that there are at least some digits
    if not re.search(r'\d', phone):
        result.add_error('phone', 'Phone must contain at least one digit')
    
    return result


def validate_company_data(data: Dict) -> ValidationResult:
    """
    Validate company registration data.
    
    Args:
        data: Dictionary containing company data
        
    Returns:
        ValidationResult with all validation errors
    """
    result = ValidationResult()
    
    # Validate required fields exist
    required_fields = ['company_name', 'owner_name', 'owner_email', 'owner_phone', 'ghl_location_id']
    for field in required_fields:
        if field not in data or not data[field]:
            result.add_error(field, f'{field} is required')
    
    # Validate company name
    if 'company_name' in data:
        name_result = validate_name(data['company_name'])
        if not name_result.is_valid:
            result.errors.update(name_result.errors)
            result.is_valid = False
    
    # Validate owner name
    if 'owner_name' in data:
        name_result = validate_name(data['owner_name'])
        if not name_result.is_valid:
            for error in name_result.errors.get('name', []):
                result.add_error('owner_name', error.replace('Name', 'Owner name'))
    
    # Validate email
    if 'owner_email' in data:
        email_result = validate_email(data['owner_email'])
        if not email_result.is_valid:
            for error in email_result.errors.get('email', []):
                result.add_error('owner_email', error)
    
    # Validate phone
    if 'owner_phone' in data:
        phone_result = validate_phone(data['owner_phone'])
        if not phone_result.is_valid:
            for error in phone_result.errors.get('phone', []):
                result.add_error('owner_phone', error)
    
    return result


def validate_lead_data(data: Dict) -> ValidationResult:
    """
    Validate lead data.
    
    Args:
        data: Dictionary containing lead data
        
    Returns:
        ValidationResult with all validation errors
    """
    result = ValidationResult()
    
    # Validate required fields exist
    required_fields = ['name', 'phone', 'company_id']
    for field in required_fields:
        if field not in data or (field != 'company_id' and not data[field]):
            result.add_error(field, f'{field} is required')
    
    # Validate name
    if 'name' in data:
        name_result = validate_name(data['name'])
        if not name_result.is_valid:
            result.errors.update(name_result.errors)
            result.is_valid = False
    
    # Validate phone
    if 'phone' in data:
        phone_result = validate_phone(data['phone'])
        if not phone_result.is_valid:
            result.errors.update(phone_result.errors)
            result.is_valid = False
    
    # Validate company_id is an integer
    if 'company_id' in data:
        try:
            int(data['company_id'])
        except (ValueError, TypeError):
            result.add_error('company_id', 'company_id must be a valid integer')
    
    return result


def validate_company_exists(company_id: int, db_session) -> ValidationResult:
    """
    Validate that a company exists in the database.
    
    Args:
        company_id: The company ID to check
        db_session: Database session
        
    Returns:
        ValidationResult indicating if the company exists
    """
    from app.models import CompanyProfile
    
    result = ValidationResult()
    
    company = db_session.query(CompanyProfile).filter_by(id=company_id).first()
    if not company:
        result.add_error('company_id', f'Company with id {company_id} does not exist')
    
    return result
