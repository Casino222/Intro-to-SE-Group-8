from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Order, OrderStatus, Product

class SellerOrderListTest(TestCase):
   def setUp(self):
       self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
       self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.99)
       self.order = Order.objects.create(user=self.user, total_price=10.99)
       self.order_status = OrderStatus.objects.create(order=self.order, status='PENDING')

   def test_seller_order_list_view(self):
       
       self.client.login(username='testuser', password='testpassword123')
       
       seller_order_list_url = reverse('seller_order_list')
       response = self.client.get(seller_order_list_url)
       self.assertEqual(response.status_code, 200)
       self.assertTemplateUsed(response, 'sellers/order_list.html')

   def test_seller_order_list_content(self):
       
       self.client.login(username='testuser', password='testpassword123')
       
       seller_order_list_url = reverse('seller_order_list')
       response = self.client.get(seller_order_list_url)
       self.assertIn(self.order, response.context['orders'])
       self.assertEqual(len(response.context['orders']), 1)

   def test_seller_order_list_redirect_if_not_logged_in(self):
       
       seller_order_list_url = reverse('seller_order_list')
       response = self.client.get(seller_order_list_url)
       self.assertRedirects(response, f'/seller/login/?next={seller_order_list_url}')