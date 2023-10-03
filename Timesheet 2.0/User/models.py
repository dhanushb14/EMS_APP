from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    employee_name = models.CharField(max_length=100)
    email_id = models.EmailField(blank=False, unique=True)
    phonenumber = models.CharField(max_length=20, unique=True)
    employee_id = models.CharField(unique=True, max_length=10, primary_key=True)
    role = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['employee_name', 'phonenumber', 'role', 'email_id']

    def _str_(self):
        return self.employee_id