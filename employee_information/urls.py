from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login', auth_views.LoginView.as_view(template_name = 'employee_information/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    path('about', views.about, name="about-page"),
    path('departments', views.departments, name="department-page"),
    path('manage_departments', views.manage_departments, name="manage_departments-page"),
    path('save_department', views.save_department, name="save-department-page"),
    path('delete_department', views.delete_department, name="delete-department"),
    path('positions', views.positions, name="position-page"),
    path('manage_positions', views.manage_positions, name="manage_positions-page"),
    path('save_position', views.save_position, name="save-position-page"),
    path('delete_position', views.delete_position, name="delete-position"),
    path('employees', views.employees, name="employee-page"),
    path('manage_employees', views.manage_employees, name="manage_employees-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete-employee"),
    path('view_employee', views.view_employee, name="view-employee-page"),
    # path('time_sheet', views.time_sheet, name="time_sheet"),
    path('time_sheet_status', views.time_sheet_status, name="time_sheet_status"),
    path('timesheets_create', views.TimeSheetCreate, name='timesheets_create'),

    path('home_employee', views.home_employee, name='home_employee'),
    path('timesheet_manager', views.timesheet_manager, name='timesheet_manager'),

    path('timesheets_update', views.timesheet_update_view, name= "time-sheet-update"),
    path('download-list-data/', views.download_list_data, name='download_list_data'),
    path('view_timesheet/', views.view_timesheet, name='view_timesheet'),
    path('timesheet_scrum', views.timesheet_scrum, name='timesheet_scrum'),


]