"""GoHighLevel API integration service."""
import requests
from typing import Dict
from flask import current_app
from app.models import Lead, CompanyProfile


class GHLService:
    """Service for GoHighLevel API integration."""
    
    def __init__(self):
        """Initialize GHL service with API credentials."""
        self.api_key = current_app.config['GHL_API_KEY']
        self.base_url = current_app.config['GHL_API_BASE_URL']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def build_contact_payload(self, lead: Lead, company: CompanyProfile) -> Dict:
        """
        Build GHL contact payload from lead and company data.
        
        Args:
            lead: Lead instance
            company: CompanyProfile instance
            
        Returns:
            Dictionary with GHL contact payload
        """
        # Parse name into first and last name
        name_parts = lead.name.strip().split(maxsplit=1)
        first_name = name_parts[0] if name_parts else lead.name
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        payload = {
            'firstName': first_name,
            'lastName': last_name,
            'phone': lead.phone,
            'tags': ['old_lead_reactivation'],
            'customFields': {
                'company_name': company.company_name,
                'owner_name': company.owner_name,
                'owner_phone': company.owner_phone,
                'owner_email': company.owner_email
            },
            'source': 'Lead Reactivation System'
        }
        
        # Add notes if present
        if lead.notes:
            payload['notes'] = lead.notes
        
        return payload
    
    def create_contact(self, location_id: str, contact_data: Dict) -> Dict:
        """
        Create a contact in GoHighLevel.
        
        Args:
            location_id: GHL location ID
            contact_data: Contact payload
            
        Returns:
            API response dictionary
            
        Raises:
            Exception: If API call fails
        """
        url = f'{self.base_url}/contacts/'
        
        # Add location ID to headers
        headers = self.headers.copy()
        headers['Location-Id'] = location_id
        
        try:
            response = requests.post(url, json=contact_data, headers=headers, timeout=30)
            
            # Check for errors
            if response.status_code >= 400:
                error_msg = f'GHL API error: {response.status_code} - {response.text}'
                raise Exception(error_msg)
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception('GHL API request timed out')
        except requests.exceptions.ConnectionError:
            raise Exception('Failed to connect to GHL API')
        except requests.exceptions.RequestException as e:
            raise Exception(f'GHL API request failed: {str(e)}')
    
    def handle_api_error(self, response) -> str:
        """
        Handle and format API error responses.
        
        Args:
            response: requests Response object
            
        Returns:
            Formatted error message
        """
        try:
            error_data = response.json()
            if 'message' in error_data:
                return f"GHL API Error: {error_data['message']}"
            return f"GHL API Error: {response.text}"
        except Exception:
            return f"GHL API Error: Status {response.status_code}"
