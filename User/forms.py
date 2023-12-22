from django import forms
from .models import Employee



class EmployeeSignUpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id','employee_name','email_id','phonenumber','password']
