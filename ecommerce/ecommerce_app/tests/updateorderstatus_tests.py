from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Order, OrderStatus, Product

class UpdateOrderStatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.99)
        self.order = Order.objects.create(user=self.user, total_price=10.99)
        self.order_status = OrderStatus.objects.create(order=self.order, status='PENDING')

    def test_update_order_status_view(self):
        self.client.login(username='testuser', password='testpassword123')
        update_order_status_url = reverse('update_order_status', kwargs={'order_id': self.order.id})
        response = self.client.get(update_order_status_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_order_status.html')

    def test_update_order_status_valid_data(self):
        self.client.login(username='testuser', password='testpassword123')
        update_order_status_url = reverse('update_order_status', kwargs={'order_id': self.order.id})
        response = self.client.post(update_order_status_url, {'status': 'SHIPPED'})
        self.assertEqual(response.status_code, 302)  
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'SHIPPED')
        self.assertTrue(OrderStatus.objects.filter(order=self.order, status='SHIPPED').exists())

    def test_update_order_status_redirect_if_not_logged_in(self):
        update_order_status_url = reverse('update_order_status', kwargs={'order_id': self.order.id})
        response = self.client.get(update_order_status_url)
        self.assertRedirects(response, '/seller/login/')
