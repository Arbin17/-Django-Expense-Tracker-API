from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.models import ExpenseIncome
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create sample expense/income data'
    
    def handle(self, *args, **options):
        # Create test users
        user1, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        if created:
            user1.set_password('password123')
            user1.save()
        
        # Create sample expenses
        ExpenseIncome.objects.create(
            user=user1,
            title='Grocery Shopping',
            description='Weekly groceries',
            amount=Decimal('100.00'),
            transaction_type='debit',
            tax=Decimal('10.00'),
            tax_type='flat'
        )
        
        ExpenseIncome.objects.create(
            user=user1,
            title='Salary',
            description='Monthly salary',
            amount=Decimal('3000.00'),
            transaction_type='credit',
            tax=Decimal('5.00'),
            tax_type='percentage'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data')
        )