from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import (
    Employee, Payroll, FinanceAccount, Transaction, FeeStructure,
    StudentFeePayment, Inventory
)

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class EmployeeSerializer(serializers.ModelSerializer):
            class Meta:
                model = Employee
                fields = '__all__'
        return EmployeeSerializer

class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class EmployeeSerializer(serializers.ModelSerializer):
            class Meta:
                model = Employee
                fields = '__all__'
        return EmployeeSerializer

class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class PayrollSerializer(serializers.ModelSerializer):
            class Meta:
                model = Payroll
                fields = '__all__'
        return PayrollSerializer

class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class PayrollSerializer(serializers.ModelSerializer):
            class Meta:
                model = Payroll
                fields = '__all__'
        return PayrollSerializer

class FinanceAccountListView(generics.ListAPIView):
    queryset = FinanceAccount.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class FinanceAccountSerializer(serializers.ModelSerializer):
            class Meta:
                model = FinanceAccount
                fields = '__all__'
        return FinanceAccountSerializer

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class TransactionSerializer(serializers.ModelSerializer):
            class Meta:
                model = Transaction
                fields = '__all__'
        return TransactionSerializer

class FeeStructureListView(generics.ListAPIView):
    queryset = FeeStructure.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class FeeStructureSerializer(serializers.ModelSerializer):
            class Meta:
                model = FeeStructure
                fields = '__all__'
        return FeeStructureSerializer

class StudentFeePaymentListView(generics.ListAPIView):
    queryset = StudentFeePayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class StudentFeePaymentSerializer(serializers.ModelSerializer):
            class Meta:
                model = StudentFeePayment
                fields = '__all__'
        return StudentFeePaymentSerializer

class ProcessFeePaymentView(generics.CreateAPIView):
    queryset = StudentFeePayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class StudentFeePaymentSerializer(serializers.ModelSerializer):
            class Meta:
                model = StudentFeePayment
                fields = '__all__'
        return StudentFeePaymentSerializer

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class InventorySerializer(serializers.ModelSerializer):
            class Meta:
                model = Inventory
                fields = '__all__'
        return InventorySerializer

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from rest_framework import serializers
        class InventorySerializer(serializers.ModelSerializer):
            class Meta:
                model = Inventory
                fields = '__all__'
        return InventorySerializer
