# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import Employee
# from django.contrib.auth import get_user_model

# class EmployeeCreateViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.signup_url = reverse('User:employee_create')
#         self.login_url = reverse('User:login')

#     def test_signup_get_request(self):
#         response = self.client.get(self.signup_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'employee_information/signup.html')

#     def test_valid_user_signup(self):
#         data = {
#             'employee_id': '12345',
#             'employee_name': 'John Doe',
#             'email_id': 'john.doe@example.com',
#             'phonenumber': '1234567890',
#             'password': 'testpassword',
#         }
#         response = self.client.post(self.signup_url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(response.context['account_created'])
#         self.assertEqual(Employee.objects.count(), 1)
#         new_employee = Employee.objects.get(employee_id=data['employee_id'])
#         self.assertEqual(new_employee.employee_name, data['employee_name'])

#     def test_invalid_user_signup(self):
#             data = {}
#             response = self.client.post(self.signup_url, data)
#             self.assertEqual(response.status_code, 200)
#             self.assertFalse(response.context['account_created'])
#             self.assertIn('errors', response.context)
        
            

# class EmployeeLoginViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('User:login')


#         self.test_user = get_user_model().objects.create_user(
#             employee_id='12345',
#             employee_name='Test User',
#             email_id='testuser@example.com',
#             phonenumber='1234567890',
#             password='testpassword'
#         )

#     def test_login_get_request(self):
#         response = self.client.get(self.login_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'employee_information/login.html')
    
#     def test_valid_user_login(self):
#         data = {
#              'employee_id' : '12345',
#              'password' : 'testpassword'
#         }
#         response = self.client.post(self.login_url,data)
#         self.assertEqual(response.status_code,200)
#         self.assertRedirects(response, expected_url=reverse('home-page'))
    
#     def test_invalid_user_login(self):
#         data = {}
#         response = self.client.post(self.login_url,data)
#         self.assertEqual(response.status_code,200)
#         self.assertContains(response, 'Invalid login credentials! Please try again.')