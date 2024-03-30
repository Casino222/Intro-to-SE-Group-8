from django.test import TestCase
from django.contrib.auth.models import User
from ecommerce_app.models import Order
from ecommerce_app.order_management import view_order_history, track_order_status

class OrderManagementTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')
        self.order1 = Order.objects.create(user=self.user, status='shipped')
        self.order2 = Order.objects.create(user=self.user, status='delivered')
        self.order3 = Order.objects.create(user=self.user, status='processing')

    def test_view_order_history(self):
        orders = view_order_history(self.user)
        self.assertEqual(len(orders), 3)
        self.assertIn(self.order1, orders)
        self.assertIn(self.order2, orders)
        self.assertIn(self.order3, orders)

    def test_track_order_status(self):
        status1 = track_order_status(self.order1.id)
        self.assertEqual(status1, 'shipped')

        status2 = track_order_status(self.order2.id)
        self.assertEqual(status2, 'delivered')

        status3 = track_order_status(self.order3.id)
        self.assertEqual(status3, 'processing')

    def test_track_order_status_invalid_order_id(self):
        invalid_order_id = 1000 
        status = track_order_status(invalid_order_id)
        self.assertIsNone(status)

    def test_track_order_status_nonexistent_order(self):
        nonexistent_order = Order.objects.create(user=self.user, status='cancelled')
        nonexistent_order_id = nonexistent_order.id
        nonexistent_order.delete()  
        status = track_order_status(nonexistent_order_id)
        self.assertIsNone(status)

    def test_view_order_history_empty(self):
        user_without_orders = User.objects.create_user(username='user_no_orders', email='no_orders@example.com', password='password')
        orders = view_order_history(user_without_orders)
        self.assertEqual(len(orders), 0)
