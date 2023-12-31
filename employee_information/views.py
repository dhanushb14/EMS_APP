from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from datetime import datetime
import datetime
from dotenv import load_dotenv
import smtplib
import os
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from User.models import Employee
from django.contrib import messages
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TimeSheet, LeaveRequest, Teams
from .forms import EmployeeForm, LeaveRequestForm
from .filters import FilterForm
import json
from django.views.decorators.http import require_http_methods
from User.models import Employee
from django.http import HttpResponse
import csv
from django.core.paginator import Paginator
import json
import openpyxl
import pandas as pd
import re
import csv
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from django.http import HttpResponse
from django.http import FileResponse
from tempfile import NamedTemporaryFile


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


# def login_user(request):
#     logout(request)
#     resp = {"status": 'failed', 'msg': ''}
#     username = ''
#     password = ''
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']
#         print(username, password)

#         user = authenticate(username=username, password=password)
#         print(user)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 resp['status'] = 'success'
#             else:
#                 resp['msg'] = "Incorrect username or password"
#         else:
#             resp['msg'] = "Incorrect username or password"
#     return HttpResponse(json.dumps(resp), content_type='application/json')

# Logout


# Create your views here.


@login_required
def home(request):
    current_user = request.user.employee_name
    print("current_user", current_user)
    model = TimeSheet
    data_result = model.objects.filter(username=current_user).order_by('-start_date')[:4]
    leave_requests = LeaveRequest.objects.filter(employee=request.user)[:4]
    # result_list = list(model.objects.filter(username=current_user).order_by('-start_date')) + list(LeaveRequest.objects.filter(employee=request.user).order_by('-start_date'))
    # Calculate the start and end dates for the current month
    current_date = datetime.now()
    start_of_month = current_date.replace(day=1)
    end_of_month = start_of_month + relativedelta(months=1, days=-1) 

    # Modify the query to filter by the start_date within the current month
    result_list = list(model.objects.filter(username=current_user, start_date__gte=start_of_month, start_date__lte=end_of_month).order_by('-start_date')) + list(LeaveRequest.objects.filter(employee=request.user, start_date__gte=start_of_month, start_date__lte=end_of_month).order_by('-start_date'))
    print(result_list)
    paginator = Paginator(data_result, 5)  # Show 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    teams = Teams.objects.all()
    employees = Employee.objects.all()
    try:
        team_member = Teams.objects.get(scrum_master_id = request.user.id)
        employe_team = [i.employee_name for i in team_member.team_members.all()]
    except:
        team_member = None
    
    scrum_team = [(scrum.scrum_master, scrum.team_name) for scrum in teams if request.user.employee_name in [employee.employee_name for employee in scrum.team_members.all()]]
    
    manager = [employee for employee in employees if employee.role == "manager"]
    admin = [admin for admin in employees if admin.role == "superadmin"]
    if scrum_team:
        scrum_master = Employee.objects.get(employee_name = scrum_team[0][0].employee_name)
    else:
        scrum_master = None
    
    context = {
        'page_title': 'Home',
        'employees': employees,
        
        
        'scrum_emp': teams,
        'scrum_master': scrum_master,
        'allManagers': manager,
        'data_result': result_list,
        
        
        'total_employee': len(Employee.objects.all()),
    }
    if admin:
        context["admin"]= admin[0]
    else:
        context["admin"]= None
    if manager:
        context["manager"]= manager[0]
    else:
        context["manager"]= None
    if scrum_team:
        context['scrum_team'] = scrum_team[0][1]
    else:
        context['scrum_team'] = None
    
    if team_member:
        context['member_team_name'] = team_member.team_name
        context['team_member'] = employe_team
    else:
        context['member_team_name'] = None
        context['team_member'] = None
    print("context",context)
    return render(request, 'employee_information/home.html', context)

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
    employee_list = Employee.objects.all()

    context = {
        'employees': employee_list,
    }
    return render(request, 'employee_information/employees.html', context)


@login_required
def manage_employees(request):
    
    # employee = {}
    if request.method == 'GET':
        print("thambi")
     
     
        data = request.GET
        # code_value = data.get('id')
        # print(code_value)
        id = ''
        if 'id' in data:
            # print(True)
            id = data['id']
        if id.isnumeric():
            employee = Employee.objects.filter(employee_id=id).first()
            # print(employee)
        context = {
            'employee': employee

        }
        return render(request, 'employee_information/manage_employee.html', context)
     

@login_required
def save_employee(request):
    data = request.POST
    code_value = data.get('id')
    print("save employee", data)
    resp={"success": True}
    try:
        employee_check = Employee.objects.get(id=data['id'])
        if (employee_check):
            print('true')
            save_employee = Employee.objects.filter(id=data['id']).update(employee_id=data['code'], employee_name=data['name'],phonenumber=data['contact'], email_id=data['email'], is_active=data['status'], role=data['role'])
            #print(save_employee)
            resp['status'] = 'success'
    except:
        resp['status'] = 'failed'

    # print(json.dumps({"code": data['code'], "name": data['name'], "contact": data['contact'],"email": data['email'], "status": data['status']}))
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_employee(request):
    data = request.POST
    code_value = data.get('id')
    print(code_value)
    resp = {'status': ''}
    try:
        Employee.objects.filter(employee_id=data['id']).delete()
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
    current_user = request.user.employee_name
    print("current_user", current_user)
    model = TimeSheet
    data_result = model.objects.filter(username=current_user).order_by('-start_date')
    paginator = Paginator(data_result, 5)  # Show 10 items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        data = json.loads(request.body)
        print('2', data)
        if data["start_date"]:
            start_date = data.get('start_date')
        else:
            start_date = None
        if data['end_date']:
            end_date = data.get('end_date')
        else:
            end_date = None
        current_user = request.user.employee_name

        # Convert start_date and end_date to datetime objects
        
        if start_date and end_date:
            data = model.objects.filter(start_date__range=(
                start_date, end_date), end_date__range=(start_date, end_date))
        elif start_date:
            data = model.objects.filter(start_date__gte=start_date)
        else:
            data = model.objects.filter( end_date__lte=end_date)

        

        


        data_result = []
        # print(data.status)

        for data in data:
            if current_user == data.username:
                data_dict = {
                    "project_name": data.project_name,
                    "username": data.username,
                    "start_date": data.start_date,
                    "end_date": data.end_date,
                    "St": data.St,
                    "ot": data.ot,
                    "status": data.status,
                    "comments": data.comments
                }
                print(data_dict)
                data_result.append(data_dict)
                paginator = Paginator(data_result, 5)
                page_number = request.GET.get('page')
                data = paginator.get_page(page_number)
                response_data = {
                        'paginator': {
                            'num_pages': data.paginator.num_pages,
                            'number': data.number,  # Include the current page number
                            'has_next': data.has_next(),  # Include this
                            'has_previous': data.has_previous(),  # Include this
                            'count': data.paginator.count,
                        },
                        'results': data_result,  # The list of results
                    }

        return JsonResponse(response_data, safe=False)
    return render(request, 'employee_information/timesheet_status_bs.html', {'data_result': page_obj})


@login_required
def TimeSheetCreate(request):
    model = TimeSheet
    leave = LeaveRequest
    from datetime import datetime
    now1 = datetime.now()
    # Get the most recent past Monday
    start_date = now1 + relativedelta(weekday=MO(-1))
    # Get the next Sunday (6 days after the start_date)
    end_date = start_date + relativedelta(days=6)
    # Filter the leave objects
    #leave_date = leave.objects.filter(employee_name=request.user.employee_name, start_date__gte=start_date, end_date__lte=end_date)
    

    current_user = request.user
    context = {
        'user': current_user,
        # other context variables...
    }

    # template_name = 'employee_information/time_sheet_status.html'
    if request.method == 'POST':

        data = json.loads(request.body)
        leave_date = leave.objects.filter(
            Q(employee_name=request.user.employee_name) & 
            (Q(start_date__lte=data.get('end_date')) & Q(end_date__gte=data.get('start_date')))
        )
        

        leave_date_in = leave.objects.filter(
            Q(employee_name=request.user.employee_name, status = 'Approved') &
            (Q(start_date__lte=data.get('end_date')) & Q(end_date__gte=data.get('start_date')))
        )

        print('here')
        from datetime import datetime, timedelta 
        start_of_week9 = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        end_of_week9 = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()
        leave_dates_this_week = []
        print(start_of_week9, end_of_week9)
        
        
        for leave_request in leave_date_in:
            leave_dates_this_week.append({
                "start_date": max(leave_request.start_date, start_of_week9),
                "end_date": min(leave_request.end_date, end_of_week9)
            })
        leave_days_of_week = []

        # Iterate through the leave_dates_this_week list and add the corresponding day of the week to the list
        for leave_date9 in leave_dates_this_week:
            current_date9 = leave_date9['start_date']
            while current_date9 <= leave_date9['end_date']:
                day_of_week9 = current_date9.strftime('%A')
                if day_of_week9 not in leave_days_of_week:
                    leave_days_of_week.append(day_of_week9)
                current_date9 += timedelta(days=1)
        leave_days_of_week = [day.lower() for day in leave_days_of_week]
        # Now leave_days_of_week contains the unique days of the week for which leave has been taken
        print('leave_dates_this_week_list', leave_dates_this_week)
        print('day', leave_days_of_week)
        
        

        data["username"] = request.user.employee_name

       # if data["method_1"] != "first_fetch":  # Loading the date into db
        print("storing undo", data)
        if len(data)>7:
            
            from datetime import datetime
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            username = request.user.employee_name
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            data_status = model.objects.filter(
                start_date=start_date, username=username)
            try:
                if data_status[0].status == "uncheck":

                    model.objects.filter(start_date=start_date, username=username).update(
                        start_date= data["start_date"],
                        end_date = data["end_date"],
                        project_name= data["project_name"],
                        monday_value= data["monday_value"],
                        tuesday_value= data["tuesday_value"],
                        wednesday_value= data["wednesday_value"],
                        thursday_value= data["thursday_value"],
                        friday_value= data["friday_value"],
                        saturday_value= data["saturday_value"],
                        sunday_value= data["sunday_value"],
                        ovt_monday= data["ovt_monday"],
                        ovt_tuesday= data["ovt_tuesday"],
                        ovt_wednesday= data["ovt_wednesday"],
                        ovt_thursday= data["ovt_thursday"],
                        ovt_friday= data["ovt_friday"],
                        ovt_saturday= data["ovt_saturday"],
                        ovt_sunday= data["ovt_sunday"],
                        St= data["St"],
                        ot= data["ot"],
                        total_hour= data["total_hour"],
                        status= " ",
                        tasks= data["tasks"],
                        th_hour= data["th_hour"],
                        username = request.user.employee_name
                    )
            except Exception:

                model.objects.create(**data)

            data.pop("username", None)
            return JsonResponse(data, safe=False)
        else:    # Fetching the data with start and end date
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            username = request.user.employee_name
            
            from datetime import datetime

            # Convert start_date and end_date to datetime objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            # import pdb
            # pdb.set_trace()
            try:
            # Filter data based on start_date and end_date
                
                data = model.objects.filter(start_date=start_date, username=username )
                
                
                
                data = {
                    "start_date": data[0].start_date,
                    "end_date": data[0].end_date,
                    "project_name": data[0].project_name,
                    "monday_value": data[0].monday_value,
                    "tuesday_value": data[0].tuesday_value,
                    "wednesday_value": data[0].wednesday_value,
                    "thursday_value": data[0].thursday_value,
                    "friday_value": data[0].friday_value,
                    "saturday_value": data[0].saturday_value,
                    "sunday_value": data[0].sunday_value,
                    "ovt_monday": data[0].ovt_monday,
                    "ovt_tuesday": data[0].ovt_tuesday,
                    "ovt_wednesday": data[0].ovt_wednesday,
                    "ovt_thursday": data[0].ovt_thursday,
                    "ovt_friday": data[0].ovt_friday,
                    "ovt_saturday": data[0].ovt_saturday,
                    "ovt_sunday": data[0].ovt_sunday,
                    "St": data[0].St,
                    "ot": data[0].ot,
                    "total_hour": data[0].total_hour,
                    "status": data[0].status,
                    "tasks": data[0].tasks,
                    "th_hour": data[0].th_hour,
                    


                }
                if leave_date:
                    
                    leave_date_list = list(leave_date.values())
                    data["leave_date"] = leave_date_list
                    data["leave_start_date"] = leave_date[0].start_date
                    data["leave_end_date"] = leave_date[0].end_date
                    data["leave_status"] = leave_date[0].status
                    data["leave_date_days"] = leave_days_of_week
                    print('if condition')
                

                
            except Exception:
                try:
                    from datetime import datetime, timedelta
                    print('in')
                    
                    # Get the current date
                    current_date = datetime.now()

                    # Calculate the most recent past Monday
                    start_of_week = current_date - timedelta(days=current_date.weekday())
                    
                    if start_date == start_of_week.date() :
                         
                        
                        leave_date_list = list(leave_date.values())
                        
                        print('here1', data)
                        

                        ###############
                       
                            ####################

                        data = {
                            #  "leave_start_date": leave_start_date,
                            "leave_start_date": leave_date[0].start_date,
                            "leave_end_date": leave_date[0].end_date,
                            # "leave_end_date": leave_end_date,
                            "leave_status": leave_date[0].status,
                            "leave_date" : leave_date_list,
                            "leave_date_days": leave_days_of_week,
                        }
                        print('leave data', data)
                    else:
                        
                        if data[0]:
                            
                            pass
                        else:
                            
                            data = None
                except:
                    
                    data = None 
                
                # For testing
            # data =            {
            #     "project_name": "DHL",
            #     "monday_value": "30",
            #     "OT": "7",
            #     "Status": "Pending",
            #     "Approved_By": "",

            # }
            print('data', data)
            return JsonResponse(data, safe=False)
    if request.method == 'GET':
        #print('IN')
        return render(request, 'employee_information/timesheet_create_bs.html', context)
    if leave_date:
        context["leave_date"] = leave_date
        
    
    return render(request, 'employee_information/timesheet_create_bs.html', context)


@login_required
def timesheet_manager( request ):
     print("timesheet manager")
     model = TimeSheet
     model_user = Employee
     
     if request.user.role == "manager":
        data_user = model_user.objects.filter(employee_id=request.user.employee_id)
     print("data_user", request.user.role)
     #data = model.objects.all().order_by('-start_date')
    #  if request.user.role == "manager":
    #     data = model.objects.exclude(username=request.user.employee_name).order_by('-start_date')
     if request.user.role == "manager":
        data = model.objects.exclude(username__in=model_user.objects.filter(role="manager").values_list('employee_name', flat=True)).order_by('-start_date')
        
     elif request.user.role == "employee":
        data = model_user.objects.filter(employee_id=request.user.employee_id)
     else:
        data = model.objects.all().order_by('-start_date')
     paginator = Paginator(data, 5)  # Show 10 items per page

     page_number = request.GET.get('page')
     page_obj = paginator.get_page(page_number)
     if request.method == 'POST':
        
            data = json.loads(request.body)
            print(len(data))
            print(data)
            if len(data) ==3:
                try:
                    print("try")
                    print(data)
                    date_string_start = data["start_date"].replace("Sept", "Sep")
                    date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
                    formatted_date_start = date_object.strftime("%Y-%m-%d")
                    model.objects.filter(start_date=formatted_date_start, project_name=data["project_name"]).update(status="Pending", comments=" ")
                    return JsonResponse({"message": "Update successful", "data": "Pending"}, status=200)
                except Exception:
                    print("except")
                    try:
                        date_object = datetime.strptime(data["start_date"], "%b. %d, %Y")
                        print(date_object)
                        formatted_date_start = date_object.strftime("%Y-%m-%d")
                        model.objects.filter(start_date=formatted_date_start, project_name=data["project_name"]).update(status="Pending", comments=" ")
                        return JsonResponse({"message": "Update successful", "data": "Pending"}, status=200)
                    except Exception:
                        model.objects.filter(start_date=data["start_date"], project_name=data["project_name"]).update(status="Pending", comments=" ")
                        return JsonResponse({"message": "Update successful", "data": "Pending"}, status=200)
            
        
            
            elif len(data)<=2:
            
                try:
                    from django.db.models import Q

                    values_list = data.get('project_name')

                    if request.user.role == "manager":      
                        queryset = model.objects.exclude(username__in=model_user.objects.filter(role="manager").values_list('employee_name', flat=True))
                    else:
                        queryset = model.objects.all()

                    if values_list[0] and not values_list[1] and not values_list[2] and not values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0])
                    elif not values_list[0] and values_list[1] and not values_list[2] and not values_list[3]:
                        queryset = queryset.filter(username=values_list[1])
                    elif not values_list[0] and not values_list[1] and values_list[2] and not values_list[3]:
                        queryset = queryset.filter(start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                    elif not values_list[0] and not values_list[1] and not values_list[2] and values_list[3]:
                        queryset = queryset.filter(status=values_list[3])
                    elif values_list[0] and values_list[1] and not values_list[2] and not values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], username=values_list[1])
                    elif values_list[0] and not values_list[1] and values_list[2] and not values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                    elif values_list[0] and not values_list[1] and not values_list[2] and values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], status=values_list[3])
                    elif not values_list[0] and values_list[1] and values_list[2] and not values_list[3]:
                        queryset = queryset.filter(username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                    elif not values_list[0] and values_list[1] and not values_list[2] and values_list[3]:
                        queryset = queryset.filter(username=values_list[1], status=values_list[3])
                    elif not values_list[0] and not values_list[1] and values_list[2] and values_list[3]:
                        queryset = queryset.filter(start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                    elif values_list[0] and values_list[1] and values_list[2] and not values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                    elif values_list[0] and values_list[1] and not values_list[2] and values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], username=values_list[1], status=values_list[3])
                    elif values_list[0] and not values_list[1] and values_list[2] and values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                    elif not values_list[0] and values_list[1] and values_list[2] and values_list[3]:
                        queryset = queryset.filter(username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                    elif values_list[0] and values_list[1] and values_list[2] and values_list[3]:
                        queryset = queryset.filter(project_name=values_list[0], username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                    
                    
                    
                    


                    data_result = queryset

                    print("data_result",data_result)
                    data_list = []
                    
                    for value in data_result:  # Iterate over the objects on the current page
                        data_list.append({
                            "username": value.username,
                            "start_date": value.start_date,
                            "end_date": value.end_date,
                            "project_name": value.project_name,
                            "St": value.St,
                            "ot": value.ot,
                            "status": value.status,
                            "comments": value.comments,
                            "total_hour": value.total_hour,
                        })
                    paginator = Paginator(data_list, 5)
                    data = paginator.get_page(page_number)
                    response_data = {
                        'paginator': {
                            'num_pages': data.paginator.num_pages,
                            'number': data.number,  # Include the current page number
                            'has_next': data.has_next(),  # Include this
                            'has_previous': data.has_previous(),  # Include this
                            'count': data.paginator.count,
                        },
                        'results': data_list,  # The list of results
                    }
                except Exception as e:
                    # Handle the exception here
                    
                    response_data = {'error': str(e)}
                
                
                return JsonResponse(response_data, safe=False)
            else:
                if request.method == 'POST':
                    
                    data = json.loads(request.body)
                    print("data", data)
                    emp_id = data['username']
                    project_name = data['project_name']
                    status = data['status']
                    comments = data['comment']
                    # Update the status and comments for the given emp_id and project_name
                    model.objects.filter(username=emp_id, project_name=project_name).update(status=status, comments=comments)
                    
                    print(data)
                    return JsonResponse({"message": "Update successful", "data": status}, status=200)
                else:
                    return JsonResponse({"message": "Invalid request method"}, status=400)

     return render(request, 'employee_information/timesheet_manager_bs.html', {"data":page_obj, "role":request.user.role} )

@login_required
def timesheet_update_view(request, timesheet_id):
    timesheet = get_object_or_404(TimeSheet, id=timesheet_id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=timesheet)
        if form.is_valid():
            form.save()
            return redirect('timesheet_detail', timesheet_id=timesheet.id)

    else:
        form = EmployeeForm(instance=timesheet)

    return render(request, 'timesheet_update.html', {'form': form, 'timesheet': timesheet})


@login_required
def download_list_data(request):
    if request.method == 'POST':
        print('download123')
        # Get the JSON data from the request body
        table_data = json.loads(request.body) 
        data = json.loads(request.body)
        print('table_data', table_data)
        model = TimeSheet
        model_user = Employee
        if table_data["html"] == "manager":
            print("timesheet manager 1") 
            ## Empty data
            if table_data["filter"] == "0": 
                print('inside filter')
                if request.user.role == "manager":      
                    ## Excluding all the manager data
                        data1 = model.objects.exclude(username__in=model_user.objects.filter(role="manager").values_list('employee_name', flat=True))
                else:
                    ## All the data for the admin
                        data1 = model.objects.all().order_by('-start_date')
                
                
            else:
                ## Based on filters
                try:
                    from django.db.models import Q
                    
                    values_list = data.get('project_name')
                    if request.user.role == "manager":      
                    ## Excluding all the manager data
                        data1 = model.objects.exclude(username__in=model_user.objects.filter(role="manager").values_list('employee_name', flat=True))
                    else:
                        ## Including all the data for the admin with filter
                        data1 = model.objects.all()

                        if values_list[0] and not values_list[1] and not values_list[2] and not values_list[3]:
                            data1 = data1.filter(project_name=values_list[0])
                        elif not values_list[0] and values_list[1] and not values_list[2] and not values_list[3]:
                            data1 = data1.filter(username=values_list[1])
                        elif not values_list[0] and not values_list[1] and values_list[2] and not values_list[3]:
                            data1 = data1.filter(start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                        elif not values_list[0] and not values_list[1] and not values_list[2] and values_list[3]:
                            data1 = data1.filter(status=values_list[3])
                        elif values_list[0] and values_list[1] and not values_list[2] and not values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], username=values_list[1])
                        elif values_list[0] and not values_list[1] and values_list[2] and not values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                        elif values_list[0] and not values_list[1] and not values_list[2] and values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], status=values_list[3])
                        elif not values_list[0] and values_list[1] and values_list[2] and not values_list[3]:
                            data1 = data1.filter(username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                        elif not values_list[0] and values_list[1] and not values_list[2] and values_list[3]:
                            data1 = data1.filter(username=values_list[1], status=values_list[3])
                        elif not values_list[0] and not values_list[1] and values_list[2] and values_list[3]:
                            data1 = data1.filter(start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                        elif values_list[0] and values_list[1] and values_list[2] and not values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date())
                        elif values_list[0] and values_list[1] and not values_list[2] and values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], username=values_list[1], status=values_list[3])
                        elif values_list[0] and not values_list[1] and values_list[2] and values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                        elif not values_list[0] and values_list[1] and values_list[2] and values_list[3]:
                            data1 = data1.filter(username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                        elif values_list[0] and values_list[1] and values_list[2] and values_list[3]:
                            data1 = data1.filter(project_name=values_list[0], username=values_list[1], start_date=datetime.strptime(values_list[2], "%Y-%m-%d").date(), status=values_list[3])
                except:
                    print('error passing')
                   

                    
                   
        else:
            print("timesheet status 1")
            current_user = request.user.employee_name
            if table_data["filter"]=="0":
                data1 = model.objects.filter(username=current_user).order_by('-start_date')
                print('data1', data1)
            else:
                if table_data["start_date"]:
                    start_date = table_data["start_date"]
                else:
                    start_date = None
                if table_data["end_date"]:
                    end_date = table_data["end_date"]
                else:
                    end_date = None

                if start_date and end_date:
                    data1 = model.objects.filter(start_date__range=(start_date, end_date), end_date__range=(start_date, end_date), username=current_user) 
                elif start_date:
                    data1 = model.objects.filter(start_date__gte=start_date, username=current_user) 
                else:
                    data1 = model.objects.filter(end_date__lte=end_date, username=current_user)
                print('data1', data1)


                
                

        

        # Create a HttpResponse object with the appropriate CSV header.
        headers = ['Project Name', 'Employee Name', 'Start Date',
                   'End Date', 'ST', 'OT', 'Status']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Timesheet.csv"'

        # Create a CSV writer.
        writer = csv.writer(response)
        writer.writerow(headers)

        # Write your data to the CSV writer.
        
        for timesheet in data1:
            row = [
            timesheet.project_name,
            timesheet.username,
            timesheet.start_date,
            timesheet.end_date,
            timesheet.St,
            timesheet.ot,
            timesheet.status]
            
            # Ensure each row is a list of individual values
            writer.writerow(row) 

        return response


@login_required
def view_timesheet(request):
    from datetime import timedelta
    model = TimeSheet
    print("view_timesheet")
    if request.method == 'GET':
        data = request.GET
        print("here1", data["id"])
        print(data["data-project"])
        print(data["data-start_date"])
        date_string_start = data["data-start_date"]
        try:
            date_string_start = date_string_start.replace("Sept", "Sep")

            date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
            formatted_date_start = date_object.strftime("%Y-%m-%d")
            data_retrived = model.objects.filter(
                username=data["id"], project_name=data["data-project"], start_date=formatted_date_start)
        except Exception:
            data_retrived = model.objects.filter(
                username=data["id"], project_name=data["data-project"], start_date=date_string_start)
            formatted_date_start = data["data-start_date"]
        try:
            date_string_end = data["data-end_date"]
            date_string_end = date_string_end.replace("Sept", "Sep")
            date_object = datetime.strptime(date_string_end, "%b. %d, %Y")
            formatted_date_end = date_object.strftime("%Y-%m-%d")
        except Exception:
            formatted_date_end = data["data-end_date"]

        result = list(range(0, len(data_retrived[0].tasks), 7))

        print("data_retrived", data_retrived[0].tasks)
        split_list_tasks = [data_retrived[0].tasks[i:i+7]
                            for i in range(0, len(data_retrived[0].tasks), 7)]

        print("split_list", split_list_tasks)
        if len(data_retrived[0].tasks) < 7:
            tasks = []
        else:
            tasks = data_retrived[0].tasks

        print("tasks", tasks)
        zipped_values = zip(data_retrived[0].tasks, data_retrived[0].monday_value, data_retrived[0].tuesday_value, data_retrived[0].wednesday_value,
                            data_retrived[0].thursday_value, data_retrived[0].friday_value, data_retrived[0].saturday_value, data_retrived[0].sunday_value)
        position = {
                    "start_date": formatted_date_start,
                    "end_date" : formatted_date_end,
                    "project_name": data_retrived[0].project_name,
                    "monday_value": data_retrived[0].monday_value,
                    "tuesday_value": data_retrived[0].tuesday_value,
                    "wednesday_value": data_retrived[0].wednesday_value,
                    "thursday_value": data_retrived[0].thursday_value,
                    "friday_value": data_retrived[0].friday_value,
                    "saturday_value": data_retrived[0].saturday_value,
                    "sunday_value": data_retrived[0].sunday_value,
                    "ovt_monday": data_retrived[0].ovt_monday,
                    "ovt_tuesday": data_retrived[0].ovt_tuesday,
                    "ovt_wednesday": data_retrived[0].ovt_wednesday,
                    "ovt_thursday": data_retrived[0].ovt_thursday,
                    "ovt_friday": data_retrived[0].ovt_friday,
                    "ovt_saturday": data_retrived[0].ovt_saturday,
                    "ovt_sunday": data_retrived[0].ovt_sunday,
                    "St": data_retrived[0].St,
                    "ot": data_retrived[0].ot,
                    "total_hour": data_retrived[0].total_hour,
                    "tasks": data_retrived[0].tasks,
                    "length": result,
                    "split_list": split_list_tasks,
                    "zipped_values": zipped_values,
                    "th_hour_0": data_retrived[0].th_hour[0],
                    "th_hour_1": data_retrived[0].th_hour[1],
                    "th_hour_2": data_retrived[0].th_hour[2],
                    "th_hour_3": data_retrived[0].th_hour[3],
                    "th_hour_4": data_retrived[0].th_hour[4],
                    "th_hour_5": data_retrived[0].th_hour[5],
                    "th_hour_6": data_retrived[0].th_hour[6],

                } 
        try:
            ## Leave object
            leave_date_in = LeaveRequest.objects.filter(
                Q(employee_name=data["id"]) & Q(status="Approved") &
                (Q(start_date__lte=formatted_date_end) & Q(end_date__gte=formatted_date_start))
            )
            
            if leave_date_in.exists(): 
                pass
            else:
                leave_date_in = None

            leave_dates_this_week = []
            start_of_week9 = datetime.strptime(formatted_date_start, "%Y-%m-%d").date()
            end_of_week9 = datetime.strptime(formatted_date_end, "%Y-%m-%d").date()
            for leave_request in leave_date_in:
                leave_dates_this_week.append({
                    "start_date": max(leave_request.start_date, start_of_week9),
                    "end_date": min(leave_request.end_date, end_of_week9)
                })
            leave_days_of_week = []
            for leave_date9 in leave_dates_this_week:
                current_date9 = leave_date9['start_date']
                while current_date9 <= leave_date9['end_date']:
                    day_of_week9 = current_date9.strftime('%A')
                    if day_of_week9 not in leave_days_of_week:
                        leave_days_of_week.append(day_of_week9)
                    current_date9 += timedelta(days=1)
            leave_days_of_week = [day.lower() for day in leave_days_of_week]
            print('leave', leave_date_in, data["id"], formatted_date_start, formatted_date_end, leave_days_of_week)
            leave = {
                "day": leave_days_of_week,
            }
        except:
            leave = {
                "day": ["1"],
            }


        return render(request, 'employee_information/uni_modal.html', {"position":position, 'leave': leave})
        #print(formatted_date)
    if request.method == "POST":
        model= TimeSheet
        data=json.loads(request.body)
        print("post data", data["project_name"])  
        
        print(data)  
        ## Converting time
        date_string_start = data["start_date"]
        try:
            date_string_start = date_string_start.replace("Sept", "Sep")

            date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
            formatted_date_start = date_object.strftime("%Y-%m-%d")

        except Exception:

            formatted_date_start = data["start_date"]
        try:
            date_string_end = data["end_date"]
            date_string_end = date_string_end.replace("Sept", "Sep")
            date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
            formatted_date_end = date_object.strftime("%Y-%m-%d")
        except Exception:
            formatted_date_end = data["end_date"]
        print("dateformatted_date_start: ", formatted_date_start)
        # retrived = model.objects.filter(project_name=data["project_name"],
        #                      start_date=formatted_date_start,
        #                      end_date=formatted_date_end
        #                      )
        # print("retrived: ", retrived[0].project_name)
        model.objects.filter(project_name=data["project_name"],
                             start_date=formatted_date_start,

                             ).update(
                                monday_value=data["monday_value"],
                                tuesday_value=data["tuesday_value"],
                                wednesday_value=data["wednesday_value"],
                                thursday_value=data["thursday_value"],
                                friday_value=data["friday_value"],
                                saturday_value=data["saturday_value"],
                                sunday_value=data["sunday_value"],
                                ovt_monday=data["ovt_monday"],
                                ovt_tuesday=data["ovt_tuesday"],
                                ovt_wednesday=data["ovt_wednesday"],
                                ovt_thursday=data["ovt_thursday"],
                                ovt_friday=data["ovt_friday"],
                                ovt_saturday=data["ovt_saturday"],
                                ovt_sunday=data["ovt_sunday"],
                                St=data["St"],
                                ot=data["ot"],
                                total_hour=data["total_hour"],
                                th_hour=data["th_hour"],
                                tasks=data["tasks"],
                             )
        print("return")
        return JsonResponse(data="success", safe=False)


def leave_request_manager(request):
    if request.method == 'POST':
        # print('in')
        # status = request.POST.get('status')
        # review_comments = request.POST.get('comments')
        # employee_id = request.POST.get('employee')  # Assuming 'employee_id' is the correct name

        data = json.loads(request.body)
        # print('data', data)
        employee_id = data.get('employee_id')
        id = data.get('id')
        status = data.get('status')
        comments = data['comments']
        # print("comments", comments, employee_id, id, status)
        try:
            # Retrieve the LeaveRequest based on the associated Employee
            # leave_request = LeaveRequest.objects.get(employee__id=employee_id)
            # leave_request.status = status
            # leave_request.comments = review_comments
            # leave_request.save()
            # print(request.POST)
            LeaveRequest.objects.filter(id=id).update(
                status=status, comments=comments)
            # print("success")
            data_result = {
                'message': 'success',
                'status': status,
                'comments': comments,
                'employee_id': employee_id,
            }
            # print("all success")
            return JsonResponse(data_result, safe=False)

            # messages.success(request, 'Leave request updated successfully.')
        except LeaveRequest.DoesNotExist:
            data_result = 'failed'
            # print("failed")
            return JsonResponse(data_result, safe=False)

        # Redirect to the same page or another page after processing the form
        return redirect('leave_manager')
    
    # If it's not a POST request, retrieve all leave requests
    if request.user.role=='scrummaster':
        all_leave_requests = LeaveRequest.objects.exclude(employee=request.user).exclude(employee__role='manager').order_by('-start_date')
        filter_queryset = FilterForm(request.GET,queryset=all_leave_requests)
        all_leave_requests = filter_queryset.qs
    else:
        all_leave_requests = LeaveRequest.objects.exclude(employee=request.user).order_by('-start_date')
        filter_queryset = FilterForm(request.GET,queryset=all_leave_requests)
        all_leave_requests = filter_queryset.qs
    paginator = Paginator(all_leave_requests,5)
    page = request.GET.get('page')
    paginated_results = paginator.get_page(page)
    employee_names = list(set(leave_request.employee_name for leave_request in paginated_results))
    return render(request, 'employee_information/leave_bs.html', {'filter_queryset':filter_queryset,'paginated_results':paginated_results,'employee_names':employee_names})

def leave_request_manager_model(request):
    if request.method == 'GET':
        try:
            
            data = request.GET
            employee_name = data["employee_name"].replace('"', "")
            startDate = data["startDate"].replace('"', "")
            endDate = data["endDate"].replace('"', "")
            no_of_days = data["no_of_days"].replace('"', "")
            leave_type = data["leave_type"].replace('"', "")
            description = data["description"].replace('"', "")
            status = data["status"].replace('"', "")
            comments = data["comments"].replace('"', "")
            id = data["id"].replace('"', "")
            
            data={
                "employee_name": employee_name,
                "startDate": startDate,
                "endDate": endDate,
                "no_of_days": no_of_days,
                "leave_type": leave_type,
                "description": description,
                "status": status,
                "comments": comments,
                "id": id,

            }
            print("dataaa", data)
            
        except:
            data = request.GET
            print("uni", data)
        return render(request, 'employee_information/leave_bs_uni_modal.html', {'data': data})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        print("post", data)
        
        try:
            

            try:
                LeaveRequest.objects.filter(id=int(data["id"].replace('"', ''))).update(
                
                
                comments=data["comments"],
                status=data["status"],)
                print("success")
                return JsonResponse({'message': 'ok'})
            except:
                LeaveRequest.objects.filter(id=data["id"]).update(
                
                
                comments=data["comments"],
                status=data["status"],)
                print("success")
                return JsonResponse({'message': 'ok'})
        except Exception as e:
            print("failed ", e)
            return JsonResponse({'message': 'failed'})
        print('post', data)

def user_leave_request(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user)
    paginator = Paginator(leave_requests,4)
    page = request.GET.get('page')
    paginated_results = paginator.get_page(page)
    employee = Employee.objects.get(employee_name=request.user.employee_name)
    available_leave = employee.available_leave
    try:
        print("reset available leave function called before")
        employee = get_object_or_404(Employee, employee_id=request.user.employee_id)
        employee.reset_available_leave()
        print("reset available leave function called")
        available_leave = employee.available_leave
        work_from_home = employee.work_from_home
    except:
        pass
    return render(request, 'employee_information/user_leave_request.html', {'paginated_results': paginated_results,'available_leave':available_leave, 'work_from_home': work_from_home})


def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            form.save()
            # print("Form submitted successfully")
            return redirect('leave_detail')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = LeaveRequestForm()

    return render(request, 'employee_information/leave_request_form.html', {'form': form})


def timesheet_bs(request):
    return render(request, 'employee_information/timesheet_bs.html')


def leave_manager_bs(request):
    return render(request, 'employee_information/leave_bs.html')


def timesheet_create_bs(request):
    return render(request, 'employee_information/timesheet_create_bs.html')


def signup_bs(request):
    return render(request, 'employee_information/signup.html')


def forgot_password(request):
    return render(request, 'employee_information/forgot_password.html')


load_dotenv()


def send_email(employee_email, employee_name, decrypted_password, employee_id):
    sender_email = 'intellectoglobal@gmail.com'
    sender_password = 'yawx mjxr mxqv lswr'
    subject = 'Password Recovery'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = employee_email
    message['Subject'] = subject

    body = f"Hi {employee_name},\n\nHere's your employee id: {employee_id} and password: {decrypted_password}.\n\nRegards,\nIntellecto Global Services"

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, employee_email, message.as_string())

def send_password(request):
    employee_email = request.POST.get('email')
    try:
        employee = Employee.objects.get(email_id=employee_email)
        employee_id = employee.employee_id
        employee_name = employee.employee_name
        password = employee.password
        # print(employee,employee_id,employee_name,password)
        # decrypted_password =  decrypt_password(password)
        # print(decrypted_password)
        send_email(employee_email, employee_name, password, employee_id)
        return render(request, 'employee_information/forgot_password.html', {'user_exists': True})
    except Employee.DoesNotExist:
        return render(request, 'employee_information/forgot_password.html', {'user_exists': False})

def download_data(request):
    # Get the filtered queryset based on the user's role
    print('hit download')
    if request.user.role == 'scrummaster':
        all_leave_requests = LeaveRequest.objects.exclude(employee=request.user).exclude(employee__role='manager').order_by('-start_date')
    else:
        all_leave_requests = LeaveRequest.objects.exclude(employee=request.user).order_by('-start_date')

    # Apply additional filtering using the FilterForm
    filter_queryset = FilterForm(request.GET, queryset=all_leave_requests)
    filtered_queryset = filter_queryset.qs

    # Create a response object with CSV content type
    response = HttpResponse(content_type='text/csv')

    # Set the Content-Disposition header for download
    response['Content-Disposition'] = 'attachment; filename="leave_requests.csv"'

    # Create a CSV writer using the response object
    csv_writer = csv.writer(response)

    # Write the header row
    csv_writer.writerow(['Name','Start Date', 'End Date', 'Days', 'Type','Comments','Status'])

    # Write the data rows
    for leave_request in filtered_queryset:
        csv_writer.writerow([leave_request.employee_name, leave_request.start_date, leave_request.end_date, leave_request.no_of_days, leave_request.leave_type, leave_request.comments, leave_request.status])

    return response
