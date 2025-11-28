"""Test script for company and lead forms without Redis/GHL."""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("\n" + "="*60)
    print("1. Testing Health Check...")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_register_company():
    """Test company registration."""
    print("\n" + "="*60)
    print("2. Testing Company Registration...")
    print("="*60)
    
    company_data = {
        "company_name": "ABC Roofing Company",
        "owner_name": "John Doe",
        "owner_email": "john@abcroofing.com",
        "owner_phone": "+1-555-1234",
        "ghl_location_id": "test_location_123"
    }
    
    print(f"Sending: {json.dumps(company_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/company/register",
        json=company_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return response.json().get('company_id')
    return None


def test_upload_single_lead(company_id):
    """Test single lead upload."""
    print("\n" + "="*60)
    print("3. Testing Single Lead Upload...")
    print("="*60)
    
    lead_data = {
        "name": "Jane Smith",
        "phone": "+1-555-5678",
        "notes": "Interested in roof repair - called about leak",
        "company_id": company_id
    }
    
    print(f"Sending: {json.dumps(lead_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/leads/single",
        json=lead_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 201


def test_dashboard(company_id):
    """Test dashboard endpoint."""
    print("\n" + "="*60)
    print("4. Testing Dashboard...")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/dashboard/{company_id}")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 TESTING ROOFING LEAD MANAGER (WITHOUT REDIS/GHL)")
    print("="*60)
    print("\nMake sure the Flask app is running: python run.py")
    print("Press Enter to continue...")
    input()
    
    try:
        # Test 1: Health Check
        if not test_health():
            print("\n❌ Health check failed! Make sure the app is running.")
            return
        
        # Test 2: Register Company
        company_id = test_register_company()
        if not company_id:
            print("\n❌ Company registration failed!")
            return
        
        print(f"\n✅ Company registered with ID: {company_id}")
        
        # Test 3: Upload Lead
        if not test_upload_single_lead(company_id):
            print("\n❌ Lead upload failed!")
            return
        
        print("\n✅ Lead uploaded successfully!")
        
        # Test 4: View Dashboard
        if not test_dashboard(company_id):
            print("\n❌ Dashboard failed!")
            return
        
        print("\n✅ Dashboard working!")
        
        # Summary
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour app is working correctly!")
        print("You can now:")
        print("  1. Register more companies")
        print("  2. Upload more leads")
        print("  3. Test CSV upload")
        print("  4. View dashboards")
        print("\nWhen ready, add Redis and GHL API key for full functionality.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Flask app!")
        print("Make sure you started the app with: python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
