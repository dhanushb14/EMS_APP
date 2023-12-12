import base64
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import json
from employee_information import urls
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()

key = generate_key()

def encrypt_password(password):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    encrypted_password_base64 = base64.b64encode(encrypted_password).decode()
    return encrypted_password_base64

def employee_create(request):
    model = Employee
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'password' in data:
            # data['password'] = encrypt_password(data['password'])
            data['password'] = make_password(data['password'])
        model.objects.create(**data)
        print(data)
        return JsonResponse(data, safe=True)
        
    else:
        return render(request, 'employee_information/signup.html')

def employee_list(request):
    # Check the user's role
    if request.user.role == 'Manager':
        return render(request, 'home.html')
    elif request.user.role == 'Employee':
        return render(request, 'home.html')  
    else:
        return render(request, 'unauthorized.html') 

def employee_update(request, pk):
    employee = get_object_or_404(Employee, employee_id=pk)
    if request.method == 'POST':
        # Handle the form submission and update the employee
        # This part depends on your form handling logic
        pass
    else:
        return render(request, 'home.html', {'employee': employee})
   


# def employee_delete(request, pk):
#     employee = get_object_or_404(Employee, employee_id=pk)
#     if request.method == 'POST':
#         # Handle the employee deletion
#         employee.delete()
#         return redirect('employee_list')
#     else:
#         return render(request, 'employee_confirm_delete.html', {'employee': employee})

