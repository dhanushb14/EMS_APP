from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.apps import apps
from django.db.models import Q
from datetime import datetime


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
        print("Enter your role: superadmin or scrummaster")
        if role != 'superadmin' and role != 'scrummaster':
            raise ValueError('Superuser must have role set to "superadmin or scrummaster"')

        return self.create_user(employee_id, password, role, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    email_id = models.EmailField(blank=False, unique=True)  
    phonenumber = models.CharField(max_length=20, unique=True)
    employee_id = models.CharField(unique=True, max_length=10)
    password = models.CharField(max_length=100)
    employee_role = [
        ('superadmin', 'Super Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ]
    role = models.CharField(max_length=100, default='employee',choices=employee_role)
    available_leave = models.IntegerField(default=2)
    work_from_home  = models.IntegerField(default=3)
    employee_active = [
        (True,'Active'),
        (False,'In Active')
    ]
    is_active = models.BooleanField(default=True,choices=employee_active)
    is_staff = models.BooleanField(default=False)
    employee_shift = [
        ('Morning shift', 'Morning shift'),
        ('Night shift', 'Night shift')
    ]
    shift = models.CharField(max_length = 50, choices=employee_shift)
    personal_email = models.EmailField(unique=True,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female')
        ]
    gender = models.CharField(max_length=10,choices=gender_choices,blank=True,null=True)
    blood_group_choices = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]
    blood_group = models.CharField(max_length=5,choices=blood_group_choices,blank=True,null=True)
    joining_date = models.DateField(blank=True,null=True)
    marital_status_choices= [
        ('Married','Married'),
        ('Single','Single')
    ]
    marital_status = models.CharField(choices=marital_status_choices,blank=True,null=True)
    emergency_contact = models.CharField(max_length=20, unique=True,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    father_name = models.CharField(blank=True,null=True)
    father_dob = models.DateField(blank=True,null=True)
    mother_name = models.CharField(blank=True,null=True)
    mother_dob = models.DateField(blank=True,null=True)
    bank_name = models.CharField(blank=True,null=True)
    bank_branch = models.CharField(blank=True,null=True)
    bank_account_no = models.CharField(blank=True,null=True)
    bank_ifsc_code = models.CharField(blank=True,null=True)
    bank_uan_no = models.CharField(blank=True,null=True)
    bank_nominee_name = models.CharField(blank=True,null=True)
    bank_nominee_dob = models.DateField(blank=True,null=True)
    proofs_aadhar_no = models.CharField(max_length=12,blank=True,null=True)
    proofs_pancard_no = models.CharField(max_length=10,blank=True,null=True)
    proofs_aadhar_softcopy = models.ImageField(blank=True,null=True,upload_to='images')
    proofs_pancard_softcopy = models.ImageField(blank=True,null=True,upload_to='images')
    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['employee_name', 'phonenumber', 'role', 'email_id']

    def reset_available_leave(self):
        from datetime import datetime, timedelta
        from django.utils import timezone
        print("came to reset_available_leave function in models")
        current_month = timezone.now().month
        current_year = timezone.now().year
        print(current_month)
        print(self.employee_name)
        LeaveRequest = apps.get_model('employee_information', 'LeaveRequest')
        data = LeaveRequest.objects.filter(employee_name = self.employee_name, status='Approved')
        if self.shift == 'Night shift':
            self.available_leave = 7
            self.work_from_home = 2
        else:
            self.available_leave = 24
            self.work_from_home = 0
        for i in data:
            
            print("1")
            print(i.start_date.month, current_month)
            print(i.no_of_days)

            if i.start_date.year == current_year and i.start_date.month < current_month and i.end_date.month >= current_month:
                
                # Calculate the last day of the current month
                
                if current_month == 12:
                    next_month = 1
                    next_year = current_year + 1
                else:
                    next_month = current_month + 1
                    next_year = current_year

                # Calculate the last day of the current month
                from datetime import datetime, timedelta
                last_day_of_current_month = datetime(current_year, current_month, 1)
                last_day_of_current_month_date = last_day_of_current_month.date()
                
                if i.end_date.month == current_month and i.end_date.year == current_year:
                    
                    end_date = i.end_date
                    days_in_current_month = (i.end_date - last_day_of_current_month_date).days + 1
                    # Initialize a counter for the number of days
                    working_days = 0

                    # Iterate through the days and count only if it's not a Saturday (5) or Sunday (6)
                    # current_date = days_in_current_month + timedelta(days=1)
                    current_date = last_day_of_current_month.date()
                    print('current date',current_date)
                    while current_date <= end_date:
                        if self.shift == "Night shift":
                            if current_date.weekday() not in [5, 6]:  # Check if the day is not Saturday or Sunday
                                working_days += 1
                        else:
                            if current_date.weekday() not in [6]:  # Check if the day is not Saturday or Sunday
                                working_days += 1
                        current_date += timedelta(days=1)
                        print('1')
                        
                    # Add 1 to include the last day of the current month
                            
                    days_in_current_month = working_days
                else:
                    import calendar
                    import datetime
                    
                    current_month1 = datetime.datetime.now().month
                    current_year1 = datetime.datetime.now().year
                    total_days_in_current_month = calendar.monthrange(current_year1, current_month1)[1]
                    # Initialize a counter for working days
                    working_days = 0

                    # Iterate through the days of the month and count working days
                    for day in range(1, total_days_in_current_month + 1):
                        date = datetime.date(current_year, current_month, day)
                        # Check if the day is not a Saturday (5) or Sunday (6)
                        if self.shift == "Night shift":
                            if date.weekday() not in [5, 6]:
                                working_days += 1
                        else:
                            if date.weekday() not in [6]:
                                working_days += 1

                    print("765",working_days)
                    
                    
                    days_in_current_month = working_days
                
                if i.leave_type == "Work from home":
                    self.work_from_home = self.work_from_home - days_in_current_month
                else:
                    self.available_leave = self.available_leave - days_in_current_month
            
            if i.start_date.month == current_month and i.start_date.year == current_year:
                
                if i.leave_type == "Work from home":
                    self.work_from_home = self.work_from_home - i.no_of_days
                else:
                    self.available_leave = self.available_leave - i.no_of_days
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
