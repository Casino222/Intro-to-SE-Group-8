from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile

class AddProductTest(TestCase):
   def setUp(self):
       self.add_product_url = reverse('add_product')
       self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

   def test_add_product_view(self):
 
       self.client.login(username='testuser', password='testpassword123')
       response = self.client.get(self.add_product_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'add_product.html')

   def test_add_product_valid_data(self):
       
       self.client.login(username='testuser', password='testpassword123')
       
       response = self.client.post(self.add_product_url, {'name': 'Test Product', 'description': 'Test Description', 'price': 10.99})
       self.assertEqual(response.status_code, 302)  
       self.assertTrue(Product.objects.filter(name='Test Product').exists())

   def test_add_product_invalid_data(self):
   
       self.client.login(username='testuser', password='testpassword123')
       
       response = self.client.post(self.add_product_url, {'name': '', 'description': '', 'price': 'invalid'})
       self.assertEqual(response.status_code, 200)
       self.assertFormError(response, 'form', 'name', 'This field is required.')
       self.assertFormError(response, 'form', 'description', 'This field is required.')
       self.assertFormError(response, 'form', 'price', 'Enter a number.')

   def test_add_product_redirect_if_not_logged_in(self):
       response = self.client.get(self.add_product_url)
       self.assertRedirects(response, '/seller/login/?next=/seller/add_product/')