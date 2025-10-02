from django.db import models
from django.conf import settings
from students.models import Student, Department
from faculty.models import Faculty

class Employee(models.Model):
    """Employee Information for HR Management"""
    EMPLOYEE_TYPES = (
        ('faculty', 'Faculty'),
        ('administrative', 'Administrative Staff'),
        ('technical', 'Technical Staff'),
        ('support', 'Support Staff'),
        ('contractual', 'Contractual'),
    )

    EMPLOYMENT_STATUS = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
        ('retired', 'Retired'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPES)
    designation = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, default='active')
    hire_date = models.DateField()
    contract_end_date = models.DateField(null=True, blank=True)
    probation_period_months = models.PositiveIntegerField(default=6)
    confirmation_date = models.DateField(null=True, blank=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_ifsc = models.CharField(max_length=11, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True)
    pf_number = models.CharField(max_length=20, blank=True)
    esi_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

class Payroll(models.Model):
    """Employee Payroll Management"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Deductions
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    esi_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    days_worked = models.PositiveIntegerField()
    days_absent = models.PositiveIntegerField(default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['employee', 'pay_period_start', 'pay_period_end']

    def __str__(self):
        return f"{self.employee.employee_id} - {self.pay_period_start} to {self.pay_period_end}"

class FinanceAccount(models.Model):
    """Chart of Accounts for Finance Management"""
    ACCOUNT_TYPES = (
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    )

    account_code = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent_account = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_code} - {self.account_name}"

class Transaction(models.Model):
    """Financial Transactions"""
    TRANSACTION_TYPES = (
        ('fee_payment', 'Fee Payment'),
        ('salary_payment', 'Salary Payment'),
        ('purchase', 'Purchase'),
        ('sale', 'Sale'),
        ('expense', 'Expense'),
        ('income', 'Income'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
    )

    transaction_id = models.CharField(max_length=20, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateField()
    account = models.ForeignKey(FinanceAccount, on_delete=models.CASCADE, related_name='transactions')
    reference_number = models.CharField(max_length=50, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.description} - {self.amount}"

class FeeStructure(models.Model):
    """Fee Structure for Programs"""
    program = models.ForeignKey('students.Program', on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.CharField(max_length=9)
    semester = models.PositiveIntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    admission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    development_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    laboratory_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    examination_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miscellaneous_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    late_fee_penalty = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)  # Percentage
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['program', 'academic_year', 'semester']

    def __str__(self):
        return f"{self.program.name} - {self.academic_year} Sem {self.semester}"

class StudentFeePayment(models.Model):
    """Student Fee Payments"""
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
    )

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online'),
        ('bank_transfer', 'Bank Transfer'),
        ('demand_draft', 'Demand Draft'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='backoffice_fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    late_fee_applied = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    remarks = models.TextField(blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.receipt_number} - {self.amount_paid}"

class Inventory(models.Model):
    """University Inventory Management"""
    ITEM_CATEGORIES = (
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('laboratory', 'Laboratory Equipment'),
        ('sports', 'Sports Equipment'),
        ('books', 'Books'),
        ('stationery', 'Stationery'),
        ('maintenance', 'Maintenance Supplies'),
        ('other', 'Other'),
    )

    ITEM_STATUS = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('damaged', 'Damaged'),
        ('disposed', 'Disposed'),
    )

    item_code = models.CharField(max_length=20, unique=True)
    item_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=ITEM_CATEGORIES)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=200, blank=True)
    warranty_period_months = models.PositiveIntegerField(default=0)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ITEM_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.item_code} - {self.item_name}"
