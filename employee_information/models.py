from datetime import datetime
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.



class TimeSheet(models.Model):
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    
    monday_value = models.CharField()
    tuesday_value = models.CharField()
    wednesday_value = models.CharField()
    thursday_value = models.CharField()
    friday_value = models.CharField()
    saturday_value = models.CharField()
    sunday_value = models.CharField()

    ovt_monday = models.IntegerField()
    ovt_tuesday = models.IntegerField()
    ovt_wednesday = models.IntegerField()
    ovt_thursday = models.IntegerField()
    ovt_friday = models.IntegerField()
    ovt_saturday = models.IntegerField()
    ovt_sunday = models.IntegerField()
    tasks = ArrayField(models.CharField(max_length=255))
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
    





