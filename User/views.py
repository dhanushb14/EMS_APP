from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeSignUpForm
from django.contrib.auth import login, logout
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)


def encrypt_password(password):
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    try:
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        print('Password decrypted successfully')
        return decrypted_password
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return None


def employee_create(request):
    errors = False
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            # employee = form.save(commit=False)

            # print("Original Password:", employee.password)
            # encrypted_password = encrypt_password(
            #     employee.password)
            # print("Encrypted Password:", encrypted_password)

            # employee.password = encrypted_password.decode('utf-8')

            try:
                form.save()
                print('Form saved successfully')
                return render(request, 'employee_information/login.html')
            except Exception as e:
                print("Error saving form:", e)
        else:
            print('Form not saved. Errors:', form.errors)
            errors = form.errors
    form = EmployeeSignUpForm()
    return render(request, 'employee_information/signup.html', {'form': form, 'errors':errors})


def user_login(request):
    wrong_credentials = False
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee_password = request.POST.get('password')
        print('Credentials entered by user:', employee_id, employee_password)

        try:
            get_user = Employee.objects.get(employee_id=employee_id)
            stored_password = get_user.password
            print('Password stored in DB:', stored_password)

            # decrypted_password = decrypt_password(
            #     stored_password)
            # print("Decrypted Password:", decrypted_password)

            # if employee_password == decrypted_password:
            if employee_password == stored_password:
                login(request, get_user)
                wrong_credentials = False
                return redirect('/')
            else:
                print('Incorrect password')
                wrong_credentials = True
        except Employee.DoesNotExist:
            print('User not found')
        except Exception as e:
            print(f'Error during login: {e}')
    else:
        print('Not a POST request')

    print('Redirecting to the login template')
    return render(request, 'employee_information/login.html',{'wrong_credentials': wrong_credentials})


def user_logout(request):
    logout(request)
    return redirect('/')


def employee_list(request):
    # Check the user's role
    if request.user.role == 'Manager':
        return render(request, 'home.html')
    elif request.user.role == 'Employee':
        return render(request, 'home.html')
    else:
        return render(request, 'unauthorized.html')


def employee_update(request, pk):
    employee = get_object_or_404(Employee, employee_id=pk)

    if request.method == 'POST':
        # Handle the form submission and update the employee
        # This part depends on your form handling logic
        pass
    else:
        return render(request, 'home.html', {'employee': employee})


# def employee_delete(request, pk):
#     employee = get_object_or_404(Employee, employee_id=pk)
#     if request.method == 'POST':
#         # Handle the employee deletion
#         employee.delete()
#         return redirect('employee_list')
#     else:
#         return render(request, 'employee_confirm_delete.html', {'employee': employee})
