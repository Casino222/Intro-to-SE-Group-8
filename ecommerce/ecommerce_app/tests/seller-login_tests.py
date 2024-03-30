from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class SellerLoginTest(TestCase):
   def setUp(self):
       self.login_url = reverse('seller_login')
       self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

   def test_login_view(self):
       response = self.client.get(self.login_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'sellers/seller_login.html')

   def test_login_valid_credentials(self):
       response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
       self.assertRedirects(response, '/seller/dashboard/')

   def test_login_invalid_credentials(self):
       response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'invalidpassword'})
       self.assertEqual(response.status_code, 200)
       self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

   def test_login_redirect_if_logged_in(self):
       self.client.login(username='testuser', password='testpassword123')
       response = self.client.get(self.login_url)
       self.assertRedirects(response, '/seller/dashboard/')