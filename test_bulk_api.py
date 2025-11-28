"""Test the bulk API endpoint."""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_bulk_api():
    """Test bulk API with simple API key."""
    
    print("\n" + "="*60)
    print("Testing Bulk API Endpoint")
    print("="*60)
    
    # Prepare data
    data = {
        "leads": [
            {
                "name": "John Smith",
                "phone": "+1-555-1111",
                "notes": "Interested in new roof",
                "company_id": 1
            },
            {
                "name": "Mary Johnson",
                "phone": "+1-555-2222",
                "notes": "Repair needed",
                "company_id": 1
            },
            {
                "name": "Bob Williams",
                "phone": "+1-555-3333",
                "notes": "Free inspection",
                "company_id": 1
            }
        ]
    }
    
    # Make request with API key
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "123"  # Simple API key for testing
    }
    
    print(f"\nSending {len(data['leads'])} leads...")
    print(f"API Key: 123")
    print(f"Endpoint: {BASE_URL}/api/leads/bulk")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/leads/bulk",
            json=data,
            headers=headers
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! Bulk API is working!")
        else:
            print(f"\n❌ Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Flask app!")
        print("Make sure the app is running: python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    print("\n🧪 Bulk API Test")
    print("Make sure:")
    print("1. Flask app is running (python run.py)")
    print("2. You have at least one company registered (company_id=1)")
    print("\nPress Enter to continue...")
    input()
    
    test_bulk_api()
