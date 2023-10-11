from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from User.models import  Employee
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import TimeSheet
from .forms import EmployeeForm 
import json
from django.views.decorators.http import require_http_methods
from User.models import Employee
from django.http import HttpResponse
import csv

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


def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = authenticate(username=username, password=password)
        print(user)
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
        'total_employee': len(Employee.objects.all()),
    }
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
    employee = {}
    if request.method == 'GET':
        data = request.GET
        #code_value = data.get('id')
        #print(code_value)
        id = ''
        if 'id' in data:
            #print(True)
            id = data['id']
        if id.isnumeric():
            employee = Employee.objects.filter(employee_id=id).first()
            #print(employee)
        context = {
            'employee': employee

        }
    return render(request, 'employee_information/manage_employee.html', context)


@login_required
def save_employee(request):
    data = request.POST
    code_value = data.get('id')
    #print(code_value)
    resp={"success": True}
    try:
        employee_check = Employee.objects.get(id=data['id'])
        if (employee_check):
            save_employee = Employee.objects.filter(id=data['id']).update(employee_id=data['code'], employee_name=data['name'],phonenumber=data['contact'], email_id=data['email'], is_active=data['status'])
            #print(save_employee)
            resp['status'] = 'success'
    except:
        resp['status'] = 'failed'

    #print(json.dumps({"code": data['code'], "name": data['name'], "contact": data['contact'],"email": data['email'], "status": data['status']}))
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
    current_user = request.user
    model = TimeSheet
    data_result = model.objects.filter(username=current_user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        current_user = request.user.employee_id
        

        # Convert start_date and end_date to datetime objects
        
        
        data = model.objects.filter(start_date__range=(start_date, end_date), end_date__range=(start_date, end_date))
        
        data_result = []
        #print(data.status)
        
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
                    }
                data_result.append(data_dict)

        
        # data={n

        # place your data here
        # }

        # data = [
        #     {
        #         "project_name": "Medtronic",
        #         "start_date": "2023-1-09",
        #         "end_date": "2023-1-16",
        #         "ST": "40",
        #         "OT": "15",
        #         "Status": "Approved",
        #         "Approved_By": "Supervisor",

        #     },

        #     {
        #         "project_name": "Scotia bank",
        #         "start_date": "2023-1-09",
        #         "end_date": "2023-1-16",
        #         "ST": "35",
        #         "OT": "0",
        #         "Status": "Pending",
        #         "Approved_By": "",

        #     },

        #     {
        #         "project_name": "DHL",
        #         "start_date": "2023-9-5",
        #         "end_date": "2023-9-12",
        #         "ST": "30",
        #         "OT": "7",
        #         "Status": "Pending",
        #         "Approved_By": "",

        #     }


        # ]
        return JsonResponse(data_result, safe=False)
    return render(request, 'employee_information/time_sheet_status.html', {'data_result': data_result})


@login_required
def TimeSheetCreate(request):
    model = TimeSheet
    
    current_user = request.user
    context = {
        'user': current_user,
        # other context variables...
    }

    # template_name = 'employee_information/time_sheet_status.html'
    if request.method == 'POST':
        
        data = json.loads(request.body)
        
        data["username"] = current_user
        
       #if data["method_1"] != "first_fetch":  # Loading the date into db
        if len(data)>7:
            model.objects.create(**data)
            
            data.pop("username", None)
            return JsonResponse(data, safe=False)
        else:    # Fetching the data with start and end date
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            username = current_user
            
            from datetime import datetime

            # Convert start_date and end_date to datetime objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            #import pdb
            #pdb.set_trace()
            try:
            # Filter data based on start_date and end_date
                data = model.objects.filter(start_date=start_date, username=username)
                print("worked")
                print("project:",data[0].project_name)
                data = {
                    "start_date": data[0].start_date,
                    "end_date" : data[0].end_date,
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
                    "total_hour": data[0].total_hour
                }
            except Exception:
                data = 0
                # For testing
            # data =            {
            #     "project_name": "DHL",
            #     "monday_value": "30",
            #     "OT": "7",
            #     "Status": "Pending",
            #     "Approved_By": "",

            # }
            print("in")
            print(data)
            return JsonResponse(data, safe=False)
    if request.method == 'GET':
        #print('IN')
        return render(request, 'employee_information/time_sheet.html', context)
    return render(request, 'employee_information/time_sheet.html', context)

@login_required
def home_employee( request ):
     model = TimeSheet
     model_user = Employee
     
     data = model.objects.filter(username=request.user.employee_id)
     data_user = model_user.objects.filter(employee_id=request.user.employee_id).first()
     
     data_list = []
     for value in data:
        data_dict={
            "alert":value.status,
            "comment":value.comments,
            "project_name":value.project_name,
            "start_date":value.start_date,
            "employee_name":data_user.employee_name
        }
     
        data_list.append(data_dict)
     print(data_list)
     return render(request, 'employee_information/home_employee.html', {"data":data_list} )

@login_required
def timesheet_manager( request ):
     print("timesheet manager")
     model = TimeSheet
     data = model.objects.all()
    #  data =            [{
    #             "project_name": "DHL",
    #             "start_date": "30",
    #             "end_date": "7",
    #             "ST": "30",
    #             "OT": "7",

    #         }]
    
     
     if request.method == 'POST':
        
        data = json.loads(request.body)
        #model.objects.create(**data)
        
        if len(data)<2:
        
            try:
                print("in")
                project_name = data.get('project_name')
                data_result = model.objects.filter(project_name=project_name)
                
                print(data_result)
                data_list = []
                for value in data_result:
                    
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
            except Exception as e:
                # Handle the exception here
                print(f"An error occurred: {str(e)}")
            
            return JsonResponse(data_list, safe=False)
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
                return JsonResponse({"message": "Update successful"}, status=200)
             else:
                 return JsonResponse({"message": "Invalid request method"}, status=400)

     return render(request, 'employee_information/timesheet_manager.html', {"data":data} )

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
        # Get the JSON data from the request body
        table_data = json.loads(request.body)
        df = pd.DataFrame(table_data)

        # Create a HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="list_data.csv"'

        # Create a CSV writer.
        writer = csv.writer(response)

        # Write your data to the CSV writer.
        for row in df.values:
            writer.writerow(row)

        return response

@login_required
def view_timesheet(request):
    model=TimeSheet
    print("view_timesheet")
    if request.method == 'GET':
        data = request.GET
        print(data["id"])
        print(data["data-project"])
        print(data["data-start_date"])
        date_string_start = data["data-start_date"]
        try:
            date_string_start = date_string_start.replace("Sept", "Sep")
            
            date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
            formatted_date_start = date_object.strftime("%Y-%m-%d")
            data_retrived = model.objects.filter(username=data["id"],project_name=data["data-project"], start_date=formatted_date_start)
        except Exception:
            data_retrived = model.objects.filter(username=data["id"],project_name=data["data-project"], start_date=date_string_start)
            formatted_date_start = data["data-start_date"]
        try:
            date_string_end = data["data-end_date"]
            date_string_end = date_string_end.replace("Sept", "Sep")
            date_object = datetime.strptime(date_string_start, "%b. %d, %Y")
            formatted_date_end = date_object.strftime("%Y-%m-%d")
        except Exception:
            formatted_date_end = data["data-end_date"]
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
                    "total_hour": data_retrived[0].total_hour
                }
        print(data_retrived[0].St)
        return render(request, 'employee_information/view_timesheet.html', {"position":position})
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
                                total_hour=data["total_hour"]
                             )
        return JsonResponse(data, safe=False)
    