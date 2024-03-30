from django.test import TestCase
from django.contrib.auth.models import User
from ecommerce_app.models import Cart, Order, Product
from ecommerce_app.purchase import checkout
from ecommerce_app.models import CartItem

class CheckoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user_1', email='test@example.com', password='password')
        self.test_product = Product.objects.create(name='Test Product', price=10.00, stock=20)  
        self.cart = Cart.objects.create(user=self.user)

    def test_checkout_successful(self):
        self.cart.cartitem_set.create(product=self.test_product, quantity=3)
        payment_method = 'Credit Card'
        order = checkout(self.user.id, payment_method)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.payment_method, payment_method)
        self.assertEqual(order.products.count(), 1)
        self.assertEqual(order.total_price, 30.00)

    def test_checkout_failed_user_not_found(self):
        self.cart.delete()
        payment_method = 'Credit Card'
        with self.assertRaises(ValueError):
            checkout(self.user.id, payment_method)

    def test_checkout_failed_cart_empty(self):
        self.cart.delete()
        payment_method = 'Credit Card'
        with self.assertRaises(ValueError):
            checkout(self.user.id, payment_method)

    def test_checkout_failed_payment_method_invalid(self):
        user = User.objects.create_user(username='test_user_2', email='test2@example.com', password='password')
        cart = Cart.objects.create(user=user)

        product = Product.objects.create(name='Test Product', price=10, stock=20)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=2)

        invalid_payment_method = "Invalid Payment Method"

        with self.assertRaises(ValueError) as context:
            checkout(user.id, invalid_payment_method)

        self.assertEqual(str(context.exception), "Invalid payment method.")

    def test_checkout_failed_insufficient_stock(self):
        self.test_product.stock = 5  
        self.test_product.save()
        self.cart.cartitem_set.create(product=self.test_product, quantity=10) 
        payment_method = 'Credit Card'
        with self.assertRaises(ValueError):
            checkout(self.user.id, payment_method)

