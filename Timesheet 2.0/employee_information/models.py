from datetime import datetime
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.TextField() 
    description = models.TextField() 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.TextField() 
    description = models.TextField() 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Employees(models.Model):
    code = models.CharField(max_length=100,blank=True) 
    firstname = models.TextField() 
    middlename = models.TextField(blank=True,null= True) 
    lastname = models.TextField() 
    gender = models.TextField(blank=True,null= True) 
    dob = models.DateField(blank=True,null= True) 
    contact = models.TextField() 
    address = models.TextField() 
    email = models.TextField() 
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
    date_hired = models.DateField() 
    salary = models.FloatField(default=0) 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '
    


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

    comments = models.CharField(max_length=100)
    timesheet_status = (
        ('Approve', 'Approve'),
        ('Reject', 'Reject')
    )
    status = models.CharField(max_length=20, choices=timesheet_status)
    def __str__(self):
        return f"Time Sheet for {self.project_name} ({self.start_date} - {self.end_date})"
    





