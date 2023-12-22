from django.urls import path
from . import views

app_name = 'User'  # Change 'employee_app' to the name of your app

urlpatterns = [
    path('employee-list/', views.employee_list, name='employee_list'),
    path('employee-create/', views.employee_create, name='employee_create'),
    path('employee-update/<str:pk>/', views.employee_update, name='employee_update'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout, name='logout'),
]
