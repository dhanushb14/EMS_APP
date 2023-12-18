from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.apps import apps

class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, password=None, role=None, **extra_fields):
        if not employee_id:
            raise ValueError('The Employee ID field must be set')

        # Create an instance of the Employee model with the provided data
        employee = self.model(employee_id=employee_id, role=role, **extra_fields)
        employee.set_password(password)
        employee.save(using=self._db)
        return employee
    
    def create_superuser(self, employee_id, password=None, role=None, **extra_fields):
        # Create a superuser with the provided data
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if role != 'superadmin':
            raise ValueError('Superuser must have role set to "superadmin"')

        return self.create_user(employee_id, password, role, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    email_id = models.EmailField(blank=False, unique=True)  
    phonenumber = models.CharField(max_length=20, unique=True)
    employee_id = models.CharField(unique=True, max_length=10)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='employee')
    available_leave = models.IntegerField(default=2)
    work_from_home  = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['employee_name', 'phonenumber', 'role', 'email_id']

    def reset_available_leave(self):
        print("came to reset_available_leave function in models")
        current_month = timezone.now().month
        print(current_month)
        print(self.employee_name)
        LeaveRequest = apps.get_model('employee_information', 'LeaveRequest')
        data = LeaveRequest.objects.filter(employee_name = self.employee_name, status='Approved')
        print(data)
        
        self.available_leave = 2
        self.work_from_home = 3
        for i in data:
            
            print("1")
            print(i.start_date.month, current_month)
            
            if i.start_date.month == current_month:
                print("came to if condition")
                if i.leave_type == "Work from home":
                    self.work_from_home = self.work_from_home - 1
                else:
                    self.available_leave = self.available_leave - 1
        self.save()

    def save(self, *args, **kwargs):
        try:
            if not self.id:
                # Get the maximum id value from the existing records
                max_id = Employee.objects.aggregate(models.Max('id'))['id__max']
                self.id = 1 if max_id is None else max_id + 1
            return super(Employee, self).save(*args, **kwargs)
        except Exception:
            # Handle the error here
            pass
    def __str__(self):
        return self.employee_name
