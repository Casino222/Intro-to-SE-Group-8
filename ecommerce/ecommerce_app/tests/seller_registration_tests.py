from django.test import TestCase
from django.urls import reverse
from ecommerce_app.forms import SellerRegistrationForm
from django.contrib.auth.models import User

class SellerRegistrationTest(TestCase):
   def setUp(self):
       self.register_url = reverse('seller_register')
       self.login_url = reverse('seller_login')
       self.valid_data = {
           'username': 'testuser',
           'email': 'test@example.com',
           'password1': 'testpassword123',
           'password2': 'testpassword123'
       }
       self.invalid_data = {
           'username': '',
           'email': 'invalidemail',
           'password1': 'password',
           'password2': 'differentpassword'
       }

   def test_register_view(self):
       response = self.client.get(self.register_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'sellers/seller_register.html')

   def test_register_valid_data(self):
       response = self.client.post(self.register_url, self.valid_data)
       self.assertEqual(response.status_code, 302)  
       self.assertTrue(User.objects.filter(username='testuser').exists())

   def test_register_invalid_data(self):
       response = self.client.post(self.register_url, self.invalid_data)
       self.assertEqual(response.status_code, 200)
       self.assertFormError(response, 'form', 'username', 'This field is required.')
       self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
       self.assertFormError(response, 'form', 'password1', 'This password is too short. It must contain at least 8 characters.')
       self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

   def test_register_redirect_if_logged_in(self):
       self.client.login(username='testuser', password='testpassword123')
       response = self.client.get(self.register_url)
       self.assertRedirects(response, '/seller/dashboard/')
