from django.contrib import admin
from User.models import Employee
from .models import LeaveRequest, TimeSheet

# Register your models here.

admin.site.register(Employee)
admin.site.register(TimeSheet)
admin.site.register(LeaveRequest)
