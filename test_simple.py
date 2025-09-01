import unittest
from app import app

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("✓ Home page loads successfully")

    def test_static_files(self):
        response = self.app.get('/static/script.js')
        self.assertEqual(response.status_code, 200)
        print("✓ Static JavaScript file loads successfully")

        response = self.app.get('/static/styles.css')
        self.assertEqual(response.status_code, 200)
        print("✓ Static CSS file loads successfully")

if __name__ == '__main__':
    print("Running simple tests...")
    unittest.main()
