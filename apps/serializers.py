from rest_framework import serializers
from .models import ExpenseIncome

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'description', 'amount', 'transaction_type',
            'tax', 'tax_type', 'total', 'created_at', 'updated_at'
        ]
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_tax(self, value):
        if value < 0:
            raise serializers.ValidationError("Tax cannot be negative")
        return value

class ExpenseIncomeListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    total = serializers.ReadOnlyField()
    
    class Meta:
        model = ExpenseIncome
        fields = ['id', 'title', 'amount', 'transaction_type', 'total', 'created_at']