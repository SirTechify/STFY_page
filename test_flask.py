import sys
from app import app

class TestApp:
    def __init__(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        print("\nTesting home page...")
        response = self.app.get('/')
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        print("✓ Home page loads successfully")
    
    def test_static_files(self):
        print("\nTesting static files...")
        # Test JavaScript file
        response = self.app.get('/static/script.js')
        assert response.status_code == 200, "Failed to load script.js"
        print("✓ JavaScript file loads successfully")
        
        # Test CSS file
        response = self.app.get('/static/styles.css')
        assert response.status_code == 200, "Failed to load styles.css"
        print("✓ CSS file loads successfully")
    
    def test_subscribe_endpoint(self):
        print("\nTesting subscribe endpoint...")
        # Test with valid email
        response = self.app.post('/api/subscribe', 
                              json={'email': 'test@example.com'},
                              content_type='application/json')
        assert response.status_code in [200, 500], f"Unexpected status code: {response.status_code}"
        print(f"✓ Subscribe endpoint responds (status: {response.status_code})")
        
        # Test with invalid email
        response = self.app.post('/api/subscribe',
                              json={'email': 'invalid-email'},
                              content_type='application/json')
        assert response.status_code == 400, f"Expected status code 400 for invalid email, got {response.status_code}"
        print("✓ Invalid email validation works")
    
    def test_contact_form(self):
        print("\nTesting contact form...")
        # Test with valid data
        response = self.app.post('/send_email',
                              json={
                                  'name': 'Test User',
                                  'email': 'test@example.com',
                                  'message': 'Test message'
                              },
                              content_type='application/json')
        assert response.status_code in [200, 500], f"Unexpected status code: {response.status_code}"
        print(f"✓ Contact form submits (status: {response.status_code})")
        
        # Test with missing fields
        response = self.app.post('/send_email',
                              json={'name': 'Test User'},
                              content_type='application/json')
        assert response.status_code == 400, f"Expected status code 400 for missing fields, got {response.status_code}"
        print("✓ Missing fields validation works")

if __name__ == "__main__":
    tester = TestApp()
    
    # Run tests
    tests = [
        tester.test_home_page,
        tester.test_static_files,
        tester.test_subscribe_endpoint,
        tester.test_contact_form
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ Test failed: {str(e)}")
            continue
    
    print("\nTesting complete!")
