from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('', views.home, name="home-page"),

    path('about', views.about, name="about-page"),
#     path('departments', views.departments, name="department-page"),
#     path('manage_departments', views.manage_departments,
#          name="manage_departments-page"),
#     path('save_department', views.save_department, name="save-department-page"),
#     path('delete_department', views.delete_department, name="delete-department"),
#     path('positions', views.positions, name="position-page"),
#     path('manage_positions', views.manage_positions,
#          name="manage_positions-page"),
#     path('save_position', views.save_position, name="save-position-page"),
#     path('delete_position', views.delete_position, name="delete-position"),
    path('employees', views.employees, name="employee-page"),
    path('manage_employees', views.manage_employees,
         name="manage_employees-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete-employee"),
#     path('view_employee', views.view_employee, name="view-employee-page"),
    # path('time_sheet', views.time_sheet, name="time_sheet"),
    path('time_sheet_status', views.time_sheet_status, name="time_sheet_status"),
    path('timesheets_create', views.TimeSheetCreate, name='timesheets_create'),

    path('timesheet_manager', views.timesheet_manager, name='timesheet_manager'),

    path('timesheets_update', views.timesheet_update_view,
         name="time-sheet-update"),
    path('download-list-data/', views.download_list_data,
         name='download_list_data'),
    path('view_timesheet/', views.view_timesheet, name='view_timesheet'),
#     path('timesheet_scrum', views.timesheet_scrum, name='timesheet_scrum'),

    path('leave_manager/', views.leave_request_manager, name='leave_manager'),
    path('leave_request_manager_model/', views.leave_request_manager_model, name='leave_request_manager_model'),
    path('leave_request/', views.create_leave_request, name='leave_request'),
    path('leave_detail/', views.user_leave_request, name='leave_detail'),

    path('timesheet_bs/', views.timesheet_bs, name='timesheet_bs'),
    path('leave_bs/', views.leave_manager_bs, name='leave_bs'),
    path('timesheet_create_bs/', views.timesheet_create_bs,
         name='timesheet_create_bs'),
    path('signup/', views.signup_bs, name='signup'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send_password',views.send_password,name='send_password'),
    path('download',views.download_data,name='download'),
    path('export_data', views.export_data, name='export_data'),
    path('leave_status/', views.employee_leave_status, name='employee_leave_status'),
    path('download_leaveStatus',views.download_leaveStatus,name='download_leaveStatus'),
    path('view_export_data', views.view_export_data, name='view_export_data'),
    path('delete_image',views.delete_image, name='delete_image'),
]
