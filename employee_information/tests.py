from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from datetime import datetime
from .models import TimeSheet, LeaveRequest
from django.contrib.auth.models import User
from User.models import Employee
from employee_information.views import TimeSheetCreate, time_sheet_status, timesheet_manager
import json

class TimeSheetCreateTest(TestCase):
    # Setting up User and Creating datas in table for timesheet
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Employee.objects.create(
            employee_id='122111',
            password='12345',
            employee_name='Test User',
            email_id='testuser@gmail.com',
            phonenumber='1234567890',
            role='employee',
            available_leave=2,
            work_from_home=3,
            is_active=True,
            is_staff=False
        )
        self.timesheet = TimeSheet.objects.create(
            username='Test User',
            start_date='2023-11-20',
            end_date='2023-11-26',
            project_name='Test Project',
            status='uncheck',
            monday_value=['0'],
            tuesday_value=['0'],
            wednesday_value=['0'],
            thursday_value=['0'],
            friday_value=['0'],
            saturday_value=['0'],
            sunday_value=['0'],
            ovt_monday=0,
            ovt_tuesday=0,
            ovt_wednesday=0,
            ovt_thursday=0,
            ovt_friday=0,
            ovt_saturday=0,
            ovt_sunday=0,
            tasks=['Task1'],
            St=0,
            ot=0,
            total_hour=0,
            th_hour=['0'],
            comments='Test Comment',
        )

    # Timesheet create - Storing data in database
    def test_store_data(self):
        request = self.factory.post('timesheets_create', json.dumps({
            'start_date': '2023-11-13',
            'end_date': '2023-11-19',
            'project_name': 'Test Project',
            'monday_value': ['0'],
            'tuesday_value': ['0'],
            'wednesday_value': ['0'],
            'thursday_value': ['0'],
            'friday_value': ['0'],
            'saturday_value': ['0'],
            'sunday_value': ['0'],
            'ovt_monday': 0,
            'ovt_tuesday': 0,
            'ovt_wednesday': 0,
            'ovt_thursday': 0,
            'ovt_friday': 0,
            'ovt_saturday': 0,
            'ovt_sunday': 0,
            'tasks': ['Task1'],
            'St': 0,
            'ot': 0,
            'total_hour': 0,
            'th_hour': ['0'],
            'comments': 'Test Comment',
        }), content_type='application/json')
        request.user = self.user
        response = TimeSheetCreate(request)
        self.assertEqual(response.status_code, 200)

    # Timesheet create - Getting the data based on the date
    def test_get_data(self):
        
        request = self.factory.post('timesheets_create', json.dumps({
            'start_date': '2023-11-20',
            'end_date': '2023-11-26',
        }), content_type = 'application/json')
        request.user = self.user
        response = TimeSheetCreate(request)
        self.assertEqual(response.status_code, 200)
        
    # Timesheet create - Update data when status is uncheck
    def test_update_data(self):
        
        request = self.factory.post('timesheets_create', json.dumps({
            'start_date': '2023-11-20',
            'end_date': '2023-11-26',
            'project_name': 'Updated Project',
            'monday_value': ['0'],
            'tuesday_value': ['0'],
            'wednesday_value': ['0'],
            'thursday_value': ['0'],
            'friday_value': ['0'],
            'saturday_value': ['0'],
            'sunday_value': ['0'],
            'ovt_monday': 0,
            'ovt_tuesday': 0,
            'ovt_wednesday': 0,
            'ovt_thursday': 0,
            'ovt_friday': 0,
            'ovt_saturday': 0,
            'ovt_sunday': 0,
            'tasks': ['Task1'],
            'St': 0,
            'ot': 0,
            'total_hour': 0,
            'th_hour': ['0'],
            'comments': 'Test Comment',
            'status': 'uncheck'
        }), content_type = 'application/json' )
        request.user = self.user
        response = TimeSheetCreate(request)
        self.assertEqual(response.status_code, 200)

    def test_status_filtered (self):
        request = self.factory.post('time_sheet_status', json.dumps({
            'start_date': '2023-11-20',
            'end_date': '2023-11-26',
        }), content_type = 'application/json')
        request.user = self.user
        response = time_sheet_status(request)
        self.assertEqual(response.status_code, 200)

    def test_filter_pendingApprovals(self):
        # Project_name filter
        request = self.factory.post('timesheet_manager', json.dumps({
            'selected': 'project_name',
            'project_name': 'Updated Project'
        }), content_type = 'application/json')
        request.user = self.user
        response = timesheet_manager(request)
        self.assertEqual(response.status_code, 200)

        # Employee_nmae filter
        request = self.factory.post('timesheet_manager', json.dumps({
            'selected': 'employee_name',
            'project_name': 'Test User'
        }), content_type = 'application/json')
        request.user = self.user
        response = timesheet_manager(request)
        self.assertEqual(response.status_code, 200)

        # Start_date filter
        request = self.factory.post('timesheet_manager', json.dumps({
            'selected': 'start_date',
            'project_name': '2023-11-20'
        }), content_type = 'application/json')
        request.user = self.user
        response = timesheet_manager(request)
        self.assertEqual(response.status_code, 200)

        # status filter
        request = self.factory.post('timesheet_manager', json.dumps({
            'selected': 'status',
            'project_name': 'uncheck'
        }), content_type = 'application/json')
        request.user = self.user
        response = timesheet_manager(request)
        self.assertEqual(response.status_code, 200)

    # Checking when manager approves the timesheet
    def test_submit_pendingApprovals(self):
        request = self.factory.post('timesheet_manager', json.dumps({
            'username': 'Test User',
            'project_name': 'Updated Project',
            'status': 'Approved',
            'comment': 'Testing the Application'
        }), content_type = 'application/json')
        request.user = self.user
        response = timesheet_manager(request)
        self.assertEqual(response.status_code, 200)

        