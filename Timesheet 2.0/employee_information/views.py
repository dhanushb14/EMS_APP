from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from employee_information.models import Department, Position, Employees
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TimeSheet

import json
from django.views.decorators.http import require_http_methods
# employees = [

#     {
#         'code':1,
#         'name':"John D Smith",
#         'contact':'09123456789',
#         'address':'Sample Address only'
#     },{
#         'code':2,
#         'name':"Claire C Blake",
#         'contact':'09456123789',
#         'address':'Sample Address2 only'
#     }

# ]
# Login


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout


def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.


@login_required
def home(request):
    context = {
        'page_title': 'Home',
        'employees': employees,
        'total_department': len(Department.objects.all()),
        'total_position': len(Position.objects.all()),
        'total_employee': len(Employees.objects.all()),
    }
    return render(request, 'employee_information/home_employee.html', context)


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'employee_information/about.html', context)

# Departments


@login_required
def departments(request):
    department_list = Department.objects.all()
    context = {
        'page_title': 'Departments',
        'departments': department_list,
    }
    return render(request, 'employee_information/departments.html', context)


@login_required
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()

    context = {
        'department': department
    }
    return render(request, 'employee_information/manage_department.html', context)


@login_required
def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_department = Department.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_department = Department(
                name=data['name'], description=data['description'], status=data['status'])
            save_department.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_department(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Department.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Positions


@login_required
def positions(request):
    position_list = Position.objects.all()
    context = {
        'page_title': 'Positions',
        'positions': position_list,
    }
    return render(request, 'employee_information/positions.html', context)


@login_required
def manage_positions(request):
    position = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()

    context = {
        'position': position
    }
    return render(request, 'employee_information/manage_position.html', context)


@login_required
def save_position(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_position = Position.objects.filter(id=data['id']).update(
                name=data['name'], description=data['description'], status=data['status'])
        else:
            save_position = Position(
                name=data['name'], description=data['description'], status=data['status'])
            save_position.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_position(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Position.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
# Employees
def employees(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }
    return render(request, 'employee_information/employees.html', context)


@login_required
def manage_employees(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'employee_information/manage_employee.html', context)


@login_required
def save_employee(request):
    data = request.POST
    resp = {'status': 'failed'}
    if (data['id']).isnumeric() and int(data['id']) > 0:
        check = Employees.objects.exclude(
            id=data['id']).filter(code=data['code'])
    else:
        check = Employees.objects.filter(code=data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()
            if (data['id']).isnumeric() and int(data['id']) > 0:
                save_employee = Employees.objects.filter(id=data['id']).update(code=data['code'], firstname=data['firstname'], middlename=data['middlename'], lastname=data['lastname'], dob=data['dob'], gender=data['gender'],
                                                                               contact=data['contact'], email=data['email'], address=data['address'], department_id=dept, position_id=pos, date_hired=data['date_hired'], salary=data['salary'], status=data['status'])
            else:
                save_employee = Employees(code=data['code'], firstname=data['firstname'], middlename=data['middlename'], lastname=data['lastname'], dob=data['dob'], gender=data['gender'],
                                          contact=data['contact'], email=data['email'], address=data['address'], department_id=dept, position_id=pos, date_hired=data['date_hired'], salary=data['salary'], status=data['status'])
                save_employee.save()
            resp['status'] = 'success'
        except Exception:
            resp['status'] = 'failed'
            print(Exception)
            print(json.dumps({"code": data['code'], "firstname": data['firstname'], "middlename": data['middlename'], "lastname": data['lastname'], "dob": data['dob'], "gender": data['gender'], "contact": data['contact'],
                  "email": data['email'], "address": data['address'], "department_id": data['department_id'], "position_id": data['position_id'], "date_hired": data['date_hired'], "salary": data['salary'], "status": data['status']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_employee(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Employees.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def view_employee(request):
    employee = {}
    departments = Department.objects.filter(status=1).all()
    positions = Position.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    return render(request, 'employee_information/view_employee.html', context)



@login_required
def time_sheet_status(request):
    model = TimeSheet
    data = model.objects.all()
    print(data)
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # data={
        # place your data here
        # }

        data = [
            {
                "project_name": "Medtronic",
                "start_date": "2023-1-09",
                "end_date": "2023-1-16",
                "ST": "40",
                "OT": "15",
                "Status": "Approved",
                "Approved_By": "Supervisor",

            },

            {
                "project_name": "Scotia bank",
                "start_date": "2023-1-09",
                "end_date": "2023-1-16",
                "ST": "35",
                "OT": "0",
                "Status": "Pending",
                "Approved_By": "",

            },

            {
                "project_name": "DHL",
                "start_date": "2023-9-5",
                "end_date": "2023-9-12",
                "ST": "30",
                "OT": "7",
                "Status": "Pending",
                "Approved_By": "",

            }


        ]
        return JsonResponse(data, safe=False)
    return render(request, 'employee_information/time_sheet_status.html', {'data': data})


@login_required
def TimeSheetCreate(request):
    model = TimeSheet
    # template_name = 'employee_information/time_sheet_status.html'
    if request.method == 'POST':
        data = json.loads(request.body)
        print(len(data))
        if len(data) > 2:  # Loading the date into db
            model.objects.create(**data)
            print(data)
            return JsonResponse(data, safe=False)
        else:    # Fetching the data with start and end date
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            # For testing
            # data =            {
            #     "project_name": "DHL",
            #     "monday_value": "30",
            #     "OT": "7",
            #     "Status": "Pending",
            #     "Approved_By": "",

            # }
            return JsonResponse(data, safe=False)
    return render(request, 'employee_information/time_sheet.html')
@login_required
def home_employee( request ):
     data=[{
         "alert":"success",
         "comment":"This is the comment."
     }]
     return render(request, 'employee_information/home_employee.html', {"data":data} )
