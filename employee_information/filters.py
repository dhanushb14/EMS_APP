import django_filters
from .models import LeaveRequest, Employee
from django import forms

class FilterForm(django_filters.FilterSet):

    class Meta:
        model = LeaveRequest
        fields = ['employee_name', 'start_date', 'end_date', 'status','leave_type']

class EmployeeListFilter(django_filters.FilterSet):

    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_id', 'role', 'is_active']
