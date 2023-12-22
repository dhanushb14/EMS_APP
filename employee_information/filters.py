import django_filters
from .models import LeaveRequest
from django import forms

class FilterForm(django_filters.FilterSet):

    class Meta:
        model = LeaveRequest
        fields = ['employee_name', 'start_date', 'end_date', 'status','leave_type']
