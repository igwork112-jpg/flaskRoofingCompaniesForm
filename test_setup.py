"""Quick test to verify the application setup."""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.app import create_app
        print("✓ Flask app imports successfully")
        
        from app.models import CompanyProfile, Lead, LeadProcessingLog
        print("✓ Models import successfully")
        
        from app.services.validation import validate_name, validate_email, validate_phone
        print("✓ Validation service imports successfully")
        
        from app.services.company_service import CompanyService
        print("✓ Company service imports successfully")
        
        from app.services.lead_service import LeadService
        print("✓ Lead service imports successfully")
        
        from app.services.logging_service import LoggingService
        print("✓ Logging service imports successfully")
        
        from app.services.ghl_service import GHLService
        print("✓ GHL service imports successfully")
        
        from app.services.dashboard_service import DashboardService
        print("✓ Dashboard service imports successfully")
        
        from app.jobs.process_lead import process_lead_job
        print("✓ Background job imports successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_app_creation():
    """Test that the Flask app can be created."""
    print("\nTesting app creation...")
    
    try:
        from app.app import create_app
        app = create_app('testing')
        
        with app.app_context():
            from app.extensions import db
            # Try to create tables
            db.create_all()
            print("✓ Database tables created successfully")
        
        print("✅ App creation successful!")
        return True
        
    except Exception as e:
        print(f"❌ App creation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("ROOFING LEAD MANAGER - SETUP TEST")
    print("=" * 50)
    
    success = True
    success = test_imports() and success
    success = test_app_creation() and success
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        print("\nYou can now:")
        print("1. Set up your .env file (copy from .env.example)")
        print("2. Start Redis: redis-server")
        print("3. Run the app: python run.py")
        print("4. Start workers: python worker.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 50)
        sys.exit(1)
