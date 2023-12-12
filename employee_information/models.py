from django.db import models
from django.db import models
from django.contrib.postgres.fields import ArrayField
from User.models import Employee
from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
# Create your models here.


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
    username = models.CharField(max_length=255)

    comments = models.CharField(max_length=100)
    timesheet_status = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject'),
        ('Pending', 'Pending'),
    )
    status = models.CharField(max_length=20, choices=timesheet_status)

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
    ]
    leave_type = models.CharField(max_length=20, choices=leave_type_choices)
    description = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    leave_status_choices = [
        ('Approved', 'Approve'),
        ('Rejected', 'Reject'),
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

    def __str__(self):
        return f"{self.employee} {self.leave_type}"