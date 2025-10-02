from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),

    # Payroll URLs
    path('payroll/', views.PayrollListCreateView.as_view(), name='payroll-list-create'),
    path('payroll/<int:pk>/', views.PayrollDetailView.as_view(), name='payroll-detail'),

    # Finance URLs
    path('accounts/', views.FinanceAccountListView.as_view(), name='finance-account-list'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list-create'),

    # Fee Management URLs
    path('fee-structures/', views.FeeStructureListView.as_view(), name='fee-structure-list'),
    path('fee-payments/', views.StudentFeePaymentListView.as_view(), name='fee-payment-list'),
    path('fee-payments/pay/', views.ProcessFeePaymentView.as_view(), name='process-fee-payment'),

    # Inventory URLs
    path('inventory/', views.InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', views.InventoryDetailView.as_view(), name='inventory-detail'),
]
