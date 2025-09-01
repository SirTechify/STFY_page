import sys
import requests
from flask import Flask

def test_endpoints(base_url='http://localhost:5000'):
    """Test the application endpoints"""
    print("\n=== Testing Application Endpoints ===\n")
    
    # Test home page
    try:
        response = requests.get(f"{base_url}/")
        print(f"Home Page - Status: {response.status_code}")
        print(f"Response length: {len(response.text)} characters")
        print("✓ Home page loaded successfully" if response.status_code == 200 else "✗ Home page failed to load")
    except Exception as e:
        print(f"✗ Error testing home page: {str(e)}")
    
    # Test static files
    try:
        response = requests.get(f"{base_url}/static/script.js")
        print(f"\nStatic JS - Status: {response.status_code}")
        print("✓ JavaScript file loaded successfully" if response.status_code == 200 else "✗ JavaScript file failed to load")
        
        response = requests.get(f"{base_url}/static/styles.css")
        print(f"Static CSS - Status: {response.status_code}")
        print("✓ CSS file loaded successfully" if response.status_code == 200 else "✗ CSS file failed to load")
    except Exception as e:
        print(f"✗ Error testing static files: {str(e)}")
    
    # Test API endpoints
    test_api_endpoints(base_url)

def test_api_endpoints(base_url):
    """Test the API endpoints"""
    print("\n=== Testing API Endpoints ===\n")
    
    # Test subscribe endpoint
    try:
        # Test with valid email
        response = requests.post(
            f"{base_url}/api/subscribe",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Subscribe (valid email) - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test with invalid email
        response = requests.post(
            f"{base_url}/api/subscribe",
            json={"email": "invalid-email"},
            headers={"Content-Type": "application/json"}
        )
        print(f"\nSubscribe (invalid email) - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test with missing email
        response = requests.post(
            f"{base_url}/api/subscribe",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"\nSubscribe (missing email) - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"✗ Error testing subscribe endpoint: {str(e)}")
    
    # Test contact form endpoint
    try:
        # Test with valid data
        response = requests.post(
            f"{base_url}/send_email",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "message": "This is a test message"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"\nContact Form (valid data) - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test with missing fields
        response = requests.post(
            f"{base_url}/send_email",
            json={"name": "Test User"},
            headers={"Content-Type": "application/json"}
        )
        print(f"\nContact Form (missing fields) - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"✗ Error testing contact form: {str(e)}")

if __name__ == "__main__":
    # Use provided base URL or default to localhost:5000
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5000'
    test_endpoints(base_url)
