from datetime import datetime
from django.db import models
from django.utils import timezone
from django.db import models


# Create your models here.



class TimeSheet(models.Model):
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    
    monday_value = models.IntegerField()
    tuesday_value = models.IntegerField()
    wednesday_value = models.IntegerField()
    thursday_value = models.IntegerField()
    friday_value = models.IntegerField()
    saturday_value = models.IntegerField()
    sunday_value = models.IntegerField()

    ovt_monday = models.IntegerField()
    ovt_tuesday = models.IntegerField()
    ovt_wednesday = models.IntegerField()
    ovt_thursday = models.IntegerField()
    ovt_friday = models.IntegerField()
    ovt_saturday = models.IntegerField()
    ovt_sunday = models.IntegerField()
    St =  models.IntegerField(null=True)
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
    





