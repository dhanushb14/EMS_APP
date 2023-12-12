from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import json
from employee_information import urls
from django.urls import reverse
from django.contrib.auth.hashers import make_password

def employee_list(request):
    # Check the user's role
    if request.user.role == 'Manager':
        return render(request, 'home.html')
    elif request.user.role == 'Employee':
        return render(request, 'home.html')  
    else:
        return render(request, 'unauthorized.html') 

def employee_create(request):
    print("employee_create")
    model = Employee
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'password' in data:
                data['password'] = make_password(data['password'])
            model.objects.create(**data)
            
            return JsonResponse(data, safe=True)
        except:
            print("except")
        
    else:
        return render(request, 'employee_information/employee_signup.html')

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

