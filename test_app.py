import unittest
from app import app, mail
from unittest.mock import patch, MagicMock
import json
import os

class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        # Test the home page loads
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SirTechify', response.data)

    def test_static_files(self):
        # Test that static files are being served
        response = self.app.get('/static/script.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DOMContentLoaded', response.data)

        response = self.app.get('/static/styles.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'body', response.data)

    @patch('app.mail.send')
    def test_subscribe_endpoint_success(self, mock_send):
        """Test successful subscription"""
        # Mock the mail.send method
        mock_send.return_value = True
        
        # Test with valid email
        response = self.app.post('/api/subscribe', 
                              json={'email': 'test@example.com'},
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Successfully subscribed!')
        mock_send.assert_called_once()

    def test_subscribe_endpoint_missing_email(self):
        """Test subscription with missing email"""
        response = self.app.post('/api/subscribe', 
                              json={},
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email is required')

    @patch('app.mail.send')
    def test_contact_form_success(self, mock_send):
        """Test successful contact form submission"""
        mock_send.return_value = True
        
        test_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message'
        }
        
        response = self.app.post('/send_email',
                              json=test_data,
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Email sent successfully!')
        mock_send.assert_called_once()

    def test_contact_form_missing_fields(self):
        """Test contact form with missing required fields"""
        # Missing name
        response = self.app.post('/send_email',
                              json={
                                  'email': 'test@example.com',
                                  'message': 'Test message'
                              },
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Missing email
        response = self.app.post('/send_email',
                              json={
                                  'name': 'Test User',
                                  'message': 'Test message'
                              },
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Missing message
        response = self.app.post('/send_email',
                              json={
                                  'name': 'Test User',
                                  'email': 'test@example.com'
                              },
                              content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
