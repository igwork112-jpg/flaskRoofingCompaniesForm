"""Company service for managing company profiles."""
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models import CompanyProfile
from app.services.validation import validate_company_data


class CompanyService:
    """Service for company profile operations."""
    
    @staticmethod
    def register_company(data: dict) -> tuple[Optional[CompanyProfile], Optional[dict]]:
        """
        Register a new company profile.
        
        Args:
            data: Dictionary containing company data
            
        Returns:
            Tuple of (CompanyProfile, error_dict)
            If successful, returns (company, None)
            If failed, returns (None, error_dict)
        """
        # Validate data
        validation_result = validate_company_data(data)
        if not validation_result.is_valid:
            return None, validation_result.errors
        
        # Create company profile
        company = CompanyProfile(
            company_name=data['company_name'].strip(),
            owner_name=data['owner_name'].strip(),
            owner_email=data['owner_email'].strip(),
            owner_phone=data['owner_phone'].strip(),
            ghl_location_id=data['ghl_location_id'].strip()
        )
        
        try:
            db.session.add(company)
            db.session.commit()
            return company, None
        except IntegrityError as e:
            db.session.rollback()
            # Check if it's a duplicate email error
            if 'owner_email' in str(e.orig) or 'UNIQUE constraint' in str(e.orig):
                return None, {'owner_email': ['A company with this email already exists']}
            return None, {'database': ['An error occurred while saving the company']}
        except Exception as e:
            db.session.rollback()
            return None, {'database': [f'An unexpected error occurred: {str(e)}']}
    
    @staticmethod
    def get_company(company_id: int) -> Optional[CompanyProfile]:
        """
        Get a company profile by ID.
        
        Args:
            company_id: The company ID
            
        Returns:
            CompanyProfile or None if not found
        """
        return db.session.query(CompanyProfile).filter_by(id=company_id).first()
    
    @staticmethod
    def get_company_by_email(email: str) -> Optional[CompanyProfile]:
        """
        Get a company profile by email.
        
        Args:
            email: The owner email
            
        Returns:
            CompanyProfile or None if not found
        """
        return db.session.query(CompanyProfile).filter_by(owner_email=email).first()
