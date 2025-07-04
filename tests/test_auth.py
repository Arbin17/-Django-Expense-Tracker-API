from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration(self):
        """Test user registration with valid data"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_registration_duplicate(self):
        """Test user registration with duplicate username"""
        User.objects.create_user(username='testuser', email='test@example.com')
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_valid(self):
        """Test user login with valid credentials"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        login_data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_user_login_invalid(self):
        """Test user login with invalid credentials"""
        login_data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)