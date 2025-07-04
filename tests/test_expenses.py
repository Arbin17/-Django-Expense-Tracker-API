from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.models import ExpenseIncome
from decimal import Decimal

class ExpenseIncomeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.expense_data = {
            'title': 'Test Expense',
            'description': 'Test description',
            'amount': '100.00',
            'transaction_type': 'debit',
            'tax': '10.00',
            'tax_type': 'flat'
        }
    
    def test_create_expense(self):
        """Test creating an expense record"""
        response = self.client.post('/api/expenses/', self.expense_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpenseIncome.objects.count(), 1)
        self.assertEqual(float(response.data['total']), 110.00)
    
    def test_list_user_expenses(self):
        """Test listing user's own expenses"""
        ExpenseIncome.objects.create(user=self.user, **self.expense_data)
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_flat_tax_calculation(self):
        """Test flat tax calculation"""
        data = self.expense_data.copy()
        data['tax_type'] = 'flat'
        data['tax'] = '15.00'
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(float(response.data['total']), 115.00)
    
    def test_percentage_tax_calculation(self):
        """Test percentage tax calculation"""
        data = self.expense_data.copy()
        data['tax_type'] = 'percentage'
        data['tax'] = '10.00'  # 10%
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(float(response.data['total']), 110.00)
    
    def test_zero_tax(self):
        """Test zero tax calculation"""
        data = self.expense_data.copy()
        data['tax'] = '0.00'
        response = self.client.post('/api/expenses/', data)
        self.assertEqual(float(response.data['total']), 100.00)
    
    def test_unauthorized_access(self):
        """Test accessing API without authentication"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)