from django.db import models
from django.db import models
from django.contrib.postgres.fields import ArrayField
from User.models import Employee
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
# Create your models here.
class Teams(models.Model):
    employees = Employee.objects.all()
    scrumMaster = [sm for sm in employees if sm.role == "scrummaster"]
    members = [emp for emp in employees if (emp.role != "scrummaster" and emp.role !="manager" and emp.role !="superadmin")]
    team_name = models.CharField(max_length=255)
    scrum_master = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'employee'}, related_name='scrum_teams')
    team_members = models.ManyToManyField(Employee, related_name='teams', limit_choices_to={'role__in': ['employee', 'other_role']})

    def save(self, *args, **kwargs):
        print("save function")
        if self.scrum_master_id:  # Check if a scrum_master is set
            print("inside if")
            scrum_master = Employee.objects.get(id=self.scrum_master_id)  # Fetch the actual Employee object
            scrum_master.role = 'scrummaster'  # Change the role
            scrum_master.save()  # Save the Employee object
        super(Teams, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.scrum_master_id:  # Check if a scrum_master is set
            scrum_master = Employee.objects.get(id=self.scrum_master_id)  # Fetch the actual Employee object
            scrum_master.role = 'employee'  # Change the role or perform any other necessary actions
            scrum_master.save()  # Save the Employee object
        super(Teams, self).delete(*args, **kwargs)

    def __str__(self):
        return self.team_name

class TimeSheet(models.Model):
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    monday_value = ArrayField(models.CharField(
        max_length=255), default=['{0}'])
    tuesday_value = ArrayField(
        models.CharField(max_length=255), default=['{0}'])
    wednesday_value = ArrayField(
        models.CharField(max_length=255), default=['{0}'])
    thursday_value = ArrayField(
        models.CharField(max_length=255), default=['{0}'])
    friday_value = ArrayField(models.CharField(
        max_length=255), default=['{0}'])
    saturday_value = ArrayField(
        models.CharField(max_length=255), default=['{0}'])
    sunday_value = ArrayField(models.CharField(
        max_length=255), default=['{0}'])

    ovt_monday = models.IntegerField()
    ovt_tuesday = models.IntegerField()
    ovt_wednesday = models.IntegerField()
    ovt_thursday = models.IntegerField()
    ovt_friday = models.IntegerField()
    ovt_saturday = models.IntegerField()
    ovt_sunday = models.IntegerField()
    tasks = ArrayField(models.CharField(max_length=255))
    St = models.IntegerField(null=True)
    ot = models.IntegerField(null=True)
    total_hour = models.IntegerField()
    th_hour = ArrayField(
        models.CharField(max_length=255), default=['{0}'])
    username = models.CharField(max_length=255)

    comments = models.CharField(max_length=100)
    timesheet_status = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject'),
        ('Pending', 'Pending'),
    )
    status = models.CharField(max_length=20, choices=timesheet_status, default='Pending')

    def __str__(self):
        return f"Time Sheet for {self.project_name} ({self.start_date} - {self.end_date})"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    employee_name = models.CharField(max_length=100) 
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    leave_type_choices = [
        ('Sick leave', 'Sick leave'),
        ('Personal leave', 'Personal leave'),
        ('Unplanned leave', 'Unplanned leave'),
        ('Emergency leave', 'Emergency leave'),
        ('Project holiday', 'Project holiday'),
        ('Work from home', 'Work from home'),
    ]
    leave_type = models.CharField(max_length=20, choices=leave_type_choices)
    description = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    leave_status_choices = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ]
    status = models.CharField(
        max_length=20, choices=leave_status_choices, default='Pending')

    def save(self, *args, **kwargs):
        # Set the employee_name before saving
        self.employee_name = self.employee.employee_name

        # Calculate the number of days excluding weekends
        weekdays = 0
        current_date = self.start_date
        while current_date <= self.end_date:
            # Check if the current day is not a weekend (Monday to Friday)
            if current_date.weekday() < 5:
                weekdays += 1
            current_date += timedelta(days=1)

        # Set the no_of_days field
        self.no_of_days = weekdays

        super(LeaveRequest, self).save(*args, **kwargs)

        if self.status == 'Approved':
            self.employee.available_leave -= self.no_of_days
            self.employee.save()
        if self.status == 'Approved':
            self.employee.available_leave -= 1
            self.employee.save()

    def __str__(self):
        return f"{self.employee} {self.leave_type}"