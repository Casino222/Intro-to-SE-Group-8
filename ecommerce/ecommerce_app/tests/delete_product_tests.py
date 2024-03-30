from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Product

class DeleteProductTest(TestCase):
   def setUp(self):
       self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
       self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.99)

   def test_delete_product_view(self):
      
       self.client.login(username='testuser', password='testpassword123')
      
       delete_product_url = reverse('delete_product', kwargs={'product_id': self.product.id})
       response = self.client.get(delete_product_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'sellers/delete_product.html')

   def test_delete_product(self):
      
       self.client.login(username='testuser', password='testpassword123')
      
       delete_product_url = reverse('delete_product', kwargs={'product_id': self.product.id})
       
       response = self.client.post(delete_product_url)
       self.assertEqual(response.status_code, 302) 
       self.assertFalse(Product.objects.filter(id=self.product.id).exists())

   def test_delete_product_redirect_if_not_logged_in(self):
      
       delete_product_url = reverse('delete_product', kwargs={'product_id': self.product.id})
       response = self.client.get(delete_product_url)
       self.assertRedirects(response, f'/seller/login/?next={delete_product_url}')