from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Product

class EditProductTest(TestCase):
   def setUp(self):
       self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
       self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.99)

   def test_edit_product_view(self):
       
       self.client.login(username='testuser', password='testpassword123')
       
       edit_product_url = reverse('edit_product', kwargs={'product_id': self.product.id})
       response = self.client.get(edit_product_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'sellers/edit_product.html')

   def test_edit_product_valid_data(self):
       
       self.client.login(username='testuser', password='testpassword123')
       
       edit_product_url = reverse('edit_product', kwargs={'product_id': self.product.id})
      
       response = self.client.post(edit_product_url, {'name': 'Updated Product', 'description': 'Updated Description', 'price': 19.99})
       self.assertEqual(response.status_code, 302)  
       self.product.refresh_from_db()
       self.assertEqual(self.product.name, 'Updated Product')
       self.assertEqual(self.product.description, 'Updated Description')
       self.assertEqual(self.product.price, 19.99)

   def test_edit_product_invalid_data(self):
       
       self.client.login(username='testuser', password='testpassword123')
      
       edit_product_url = reverse('edit_product', kwargs={'product_id': self.product.id})
      
       response = self.client.post(edit_product_url, {'name': '', 'description': '', 'price': 'invalid'})
       self.assertEqual(response.status_code, 200)
       self.assertFormError(response, 'form', 'name', 'This field is required.')
       self.assertFormError(response, 'form', 'description', 'This field is required.')
       self.assertFormError(response, 'form', 'price', 'Enter a number.')

   def test_edit_product_redirect_if_not_logged_in(self):
       edit_product_url = reverse('edit_product', kwargs={'product_id': self.product.id})
       response = self.client.get(edit_product_url)
       self.assertRedirects(response, f'/seller/login/?next={edit_product_url}')