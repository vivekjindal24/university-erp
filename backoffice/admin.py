from django.contrib import admin
from .models import (
    Employee, Payroll, FinanceAccount, Transaction, FeeStructure,
    StudentFeePayment, Inventory
)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'employee_type', 'employment_status', 'hire_date')
    list_filter = ('employee_type', 'employment_status', 'department', 'hire_date')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'designation')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_period_start', 'pay_period_end', 'gross_salary', 'net_salary', 'payment_status')
    list_filter = ('payment_status', 'pay_period_start', 'employee__department')
    search_fields = ('employee__employee_id', 'employee__user__first_name')

@admin.register(FinanceAccount)
class FinanceAccountAdmin(admin.ModelAdmin):
    list_display = ('account_code', 'account_name', 'account_type', 'parent_account', 'is_active')
    list_filter = ('account_type', 'is_active')
    search_fields = ('account_code', 'account_name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'transaction_type', 'amount', 'transaction_date', 'account', 'created_by')
    list_filter = ('transaction_type', 'transaction_date', 'account__account_type')
    search_fields = ('transaction_id', 'description', 'reference_number')

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('program', 'academic_year', 'semester', 'total_fee', 'due_date', 'is_active')
    list_filter = ('academic_year', 'semester', 'is_active', 'program__department')
    search_fields = ('program__name', 'academic_year')

@admin.register(StudentFeePayment)
class StudentFeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'receipt_number', 'amount_due', 'amount_paid', 'status', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('student__student_id', 'receipt_number')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'item_name', 'category', 'status', 'purchase_date', 'assigned_to')
    list_filter = ('category', 'status', 'purchase_date')
    search_fields = ('item_code', 'item_name', 'brand', 'model')
