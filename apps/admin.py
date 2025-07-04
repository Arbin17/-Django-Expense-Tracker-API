from django.contrib import admin
from .models import ExpenseIncome

@admin.register(ExpenseIncome)
class ExpenseIncomeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'amount', 'transaction_type', 'total', 'created_at']
    list_filter = ['transaction_type', 'tax_type', 'created_at']
    search_fields = ['title', 'user__username', 'description']
    readonly_fields = ['total', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)