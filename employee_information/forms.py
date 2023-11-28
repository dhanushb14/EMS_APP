from django import forms
from User.models import Employee
from .models import LeaveRequest


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
        }

# class LeaveRequestReview(forms.ModelForm):
#     class Meta:
#         model = LeaveRequest
#         fields = ['status', 'comments']
#         widgets = {
#             'status': forms.Select(attrs={'class': 'form-select'}),
#             'comments': forms.Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control'}),
#         }


class LeaveRequestReview(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'comments']
