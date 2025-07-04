from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ExpenseIncome
from .serializers import ExpenseIncomeSerializer, ExpenseIncomeListSerializer
from .permissions import IsOwnerOrSuperuser

class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuser]
    
    def get_queryset(self):
        """
        Return objects for the current user only.
        Superusers can see all objects.
        """
        if self.request.user.is_superuser:
            return ExpenseIncome.objects.all()
        return ExpenseIncome.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use simplified serializer for list view"""
        if self.action == 'list':
            return ExpenseIncomeListSerializer
        return ExpenseIncomeSerializer
    
    def perform_create(self, serializer):
        """Set the user to the current user when creating"""
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Create a new expense/income record"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Update an existing record"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a record"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)