from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Cart, Wishlist, Product, Customer, CATEGORY_CHOICES, STATE_CHOICES, OrderPlaced, Payment
from django.test.client import Client
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from .forms import LoginForm, CustomerRegistrationForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, CustomerProfileForm

class ProductTestCase(TestCase):
    def setUp(self):
        # Create a sample product for use in multiple tests
        self.product = Product.objects.create(
            title="Test Product",
            selling_price=150.00,
            discounted_price=120.00,
            description="A sample product description",
            composition="Various materials",
            prodapp="Example use",
            category='CR',
            product_image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_product_creation(self):
        # Test product is created and can be retrieved
        product = Product.objects.get(title="Test Product")
        self.assertEqual(product.selling_price, 150.00)
        self.assertEqual(product.discounted_price, 120.00)
        self.assertEqual(product.description, "A sample product description")
        self.assertEqual(product.composition, "Various materials")
        self.assertEqual(product.prodapp, "Example use")
        self.assertEqual(product.category, 'CR')
        self.assertTrue(product.product_image, 'test_image.jpg')

    def test_product_str(self):
        # Test the string representation of the product
        self.assertEqual(str(self.product), "Test Product")

    def test_invalid_category(self):
        # Test category validation, setting an invalid category
        with self.assertRaises(ValidationError):
            invalid_product = Product(
                title="Invalid Category Product",
                selling_price=100.00,
                discounted_price=80.00,
                description="Wrong category",
                category='XYZ',  # Assuming XYZ is not a valid category
                product_image=SimpleUploadedFile(name='test_image2.jpg', content=b'', content_type='image/jpeg')
            )
            invalid_product.full_clean()  # This should raise ValidationError

class CustomerTestCase(TestCase):
    def setUp(self):
        # Set up a User instance for associating with a Customer
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.customer = Customer.objects.create(
            user=self.user,
            name="John Doe",
            locality="123 Test St",
            city="Testville",
            mobile=1234567890,
            zipcode=12345,
            state='New York'
        )

    def test_customer_creation(self):
        # Test Customer creation and field values
        customer = Customer.objects.get(name="John Doe")
        self.assertEqual(customer.user.username, "testuser")
        self.assertEqual(customer.locality, "123 Test St")
        self.assertEqual(customer.city, "Testville")
        self.assertEqual(customer.mobile, 1234567890)
        self.assertEqual(customer.zipcode, 12345)
        self.assertEqual(customer.state, 'New York')

    def test_customer_str(self):
        # Test the string representation of the customer
        self.assertEqual(str(self.customer), "John Doe")

class CartTestCase(TestCase):
    def setUp(self):
        # Creating a user
        self.user = User.objects.create_user(username='john', password='pass1234')

        # Creating two products
        self.product1 = Product.objects.create(
            title="Gaming Console",
            selling_price=299.99,
            discounted_price=249.99,
            description="A popular gaming console",
            category="MS",
            product_image="path/to/image.jpg"
        )
        self.product2 = Product.objects.create(
            title="Action Game",
            selling_price=59.99,
            discounted_price=49.99,
            description="An exciting new action game",
            category="GH",
            product_image="path/to/image2.jpg"
        )

        # Adding products to the cart
        self.cart_item1 = Cart.objects.create(user=self.user, product=self.product1, quantity=1)
        self.cart_item2 = Cart.objects.create(user=self.user, product=self.product2, quantity=2)

    def test_cart_creation(self):
        # Test if the cart items are created properly
        self.assertEqual(self.cart_item1.user.username, 'john')
        self.assertEqual(self.cart_item1.product.title, 'Gaming Console')
        self.assertEqual(self.cart_item1.quantity, 1)
        self.assertEqual(self.cart_item2.quantity, 2)

    def test_cart_total_cost(self):
        # Testing the total cost calculation for cart items
        self.assertAlmostEqual(self.cart_item1.total_cost, 249.99)
        self.assertAlmostEqual(self.cart_item2.total_cost, 99.98)

    def test_update_cart_quantity(self):
        # Test updating the quantity of cart items
        self.cart_item1.quantity = 3
        self.cart_item1.save()
        self.assertEqual(Cart.objects.get(id=self.cart_item1.id).quantity, 3)
        self.assertAlmostEqual(self.cart_item1.total_cost, 749.97)

    def test_cart_items_by_user(self):
        # Testing retrieval of cart items by user
        user_cart_items = Cart.objects.filter(user=self.user)
        self.assertEqual(len(user_cart_items), 2)

class OrderPlacedTestCase(TestCase):
    def setUp(self):
        # Creating a user
        self.user = User.objects.create_user(username='john', email='john@example.com', password='pass1234')

        # Creating a customer linked to the user
        self.customer = Customer.objects.create(
            user=self.user,
            name="John Doe",
            locality="123 Elm Street",
            city="Springfield",
            zipcode=12345,
            state="California",
            mobile=9876543210
        )

        # Creating a product
        self.product = Product.objects.create(
            title="Adventure Game",
            selling_price=60,
            discounted_price=45,
            description="A thrilling new adventure game",
            category="GH",
            product_image="path/to/image.jpg"
        )

        # Creating a payment record
        self.payment = Payment.objects.create(
            user=self.user,
            amount=90,
            razorpay_order_id="order123",
            razorpay_payment_status="captured",
            razorpay_payment_id="pay123",
            paid=True
        )

        # Placing an order
        self.order = OrderPlaced.objects.create(
            user=self.user,
            customer=self.customer,
            product=self.product,
            quantity=2,
            status='Pending',
            payment=self.payment
        )

    def test_order_creation(self):
        # Test if the order is created with correct information
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.product, self.product)
        self.assertEqual(self.order.quantity, 2)
        self.assertEqual(self.order.status, 'Pending')
        self.assertEqual(self.order.payment, self.payment)

    def test_order_total_cost(self):
        # Test the total cost calculation for the order
        expected_total = self.product.discounted_price * self.order.quantity
        self.assertAlmostEqual(self.order.total_cost, expected_total)

    def test_order_status_update(self):
        # Test updating the order status
        self.order.status = 'Delivered'
        self.order.save()
        updated_order = OrderPlaced.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'Delivered')

    def test_order_link_to_payment(self):
        # Test that the order correctly links to its payment
        self.assertTrue(self.order.payment.paid)
        self.assertEqual(self.order.payment.amount, 90)

class WishlistTestCase(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass321')

        # Create products
        self.product1 = Product.objects.create(
            title="Exciting Game",
            selling_price=30,
            discounted_price=25,
            description="Exciting new puzzle game",
            category="PN",
            product_image="path/to/image1.jpg"
        )
        self.product2 = Product.objects.create(
            title="Action Game",
            selling_price=50,
            discounted_price=45,
            description="High-paced action game",
            category="GH",
            product_image="path/to/image2.jpg"
        )

        # Create wishlist entries
        Wishlist.objects.create(user=self.user1, product=self.product1)
        Wishlist.objects.create(user=self.user1, product=self.product2)
        Wishlist.objects.create(user=self.user2, product=self.product1)

    def test_wishlist_entries(self):
        # Ensure all wishlist entries are correctly created
        user1_wishlist_count = Wishlist.objects.filter(user=self.user1).count()
        user2_wishlist_count = Wishlist.objects.filter(user=self.user2).count()
        self.assertEqual(user1_wishlist_count, 2)
        self.assertEqual(user2_wishlist_count, 1)

    def test_product_link(self):
        # Test the correct linkage of products to wishlist entries
        wishlist_entry = Wishlist.objects.get(user=self.user1, product=self.product1)
        self.assertEqual(wishlist_entry.product, self.product1)

    def test_multiple_users_wishlist(self):
        # Ensure that multiple users can add the same product to their wishlists
        self.assertTrue(Wishlist.objects.filter(product=self.product1).count(), 2)

    def test_wishlist_deletion(self):
        # Test the deletion of a wishlist entry
        Wishlist.objects.filter(user=self.user1, product=self.product1).delete()
        self.assertEqual(Wishlist.objects.filter(user=self.user1, product=self.product1).count(), 0)
        # Ensure other entries remain unaffected
        self.assertEqual(Wishlist.objects.filter(user=self.user1).count(), 1)

class PaymentTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create payment instances
        self.payment1 = Payment.objects.create(
            user=self.user,
            amount=10.99,
            razorpay_order_id='order123',
            razorpay_payment_status='Pending',
            razorpay_payment_id='payment123',
            paid=False
        )

    def test_payment_creation(self):
        # Test if the payment instance is created correctly.
        payment = Payment.objects.get(id=self.payment1.id)
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, 10.99)
        self.assertEqual(payment.razorpay_order_id, 'order123')
        self.assertEqual(payment.razorpay_payment_status, 'Pending')
        self.assertEqual(payment.razorpay_payment_id, 'payment123')
        self.assertFalse(payment.paid)

    def test_payment_update(self):
        # Test updating the payment status and check persistence
        self.payment1.razorpay_payment_status = 'Completed'
        self.payment1.paid = True
        self.payment1.save()

        updated_payment = Payment.objects.get(id=self.payment1.id)
        self.assertEqual(updated_payment.razorpay_payment_status, 'Completed')
        self.assertTrue(updated_payment.paid)

    def test_multiple_payments(self):
        # Test creating multiple payments for one user
        Payment.objects.create(
            user=self.user,
            amount=20.45,
            razorpay_order_id='order456',
            razorpay_payment_status='Pending',
            razorpay_payment_id='payment456',
            paid=False
        )
        payments = Payment.objects.filter(user=self.user)
        self.assertEqual(payments.count(), 2)

    def test_payment_deletion(self):
        # Test deletion of a payment
        Payment.objects.get(id=self.payment1.id).delete()
        with self.assertRaises(Payment.DoesNotExist):
            Payment.objects.get(id=self.payment1.id)

class CustomerRegistrationFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password1': 'Complexpass123',
            'password2': 'Complexpass123',
        }

    def test_form_valid(self):
        form = CustomerRegistrationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_form_password_match(self):
        form = CustomerRegistrationForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['password1'], form.cleaned_data['password2'])

    def test_form_password_mismatch(self):
        data = self.user_data.copy()
        data['password2'] = 'Mismatch123'
        form = CustomerRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_email(self):
        data = self.user_data.copy()
        data['email'] = 'invalid-email'
        form = CustomerRegistrationForm(data=data)
        self.assertFalse(form.is_valid())

class MyPasswordResetFormTest(TestCase):
    def test_form_valid_email(self):
        form = MyPasswordResetForm(data={'email': 'valid@example.com'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        form = MyPasswordResetForm(data={'email': 'invalid-email'})
        self.assertFalse(form.is_valid())

    def test_form_email_field_widget_class(self):
        form = MyPasswordResetForm()
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'form-control')

    def test_form_no_data(self):
        form = MyPasswordResetForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_field_label(self):
        form = MyPasswordResetForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')

class MySetPasswordFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='old_password123')
        self.user.save()

    def test_form_valid(self):
        form = MySetPasswordForm(user=self.user, data={'new_password1': 'newComplex123', 'new_password2': 'newComplex123'})
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = MySetPasswordForm(user=self.user, data={'new_password1': 'newPassword123', 'new_password2': 'differentNewPassword123'})
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors)

    def test_widget_classes(self):
        form = MySetPasswordForm(user=self.user)
        self.assertEqual(form.fields['new_password1'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['new_password2'].widget.attrs['class'], 'form-control')

    def test_form_labels(self):
        form = MySetPasswordForm(user=self.user)
        self.assertEqual(form.fields['new_password1'].label, 'New Password')
        self.assertEqual(form.fields['new_password2'].label, 'Confirm New Password')

class CustomerProfileFormTest(TestCase):
    def setUp(self):
        self.profile_data = {
            'name': 'John Doe',
            'locality': '1234 Main St',
            'city': 'Anytown',
            'mobile': '1234567890',
            'state': 'California',
            'zipcode': '90210',
        }

    def test_form_valid(self):
        form = CustomerProfileForm(data=self.profile_data)
        self.assertTrue(form.is_valid())

    def test_form_labels(self):
        form = CustomerProfileForm()
        self.assertEqual(form.fields['name'].label, 'Name')

    def test_form_field_widget_class(self):
        form = CustomerProfileForm()
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')

    def test_form_partial_data(self):
        data = {'name': 'John Doe'}
        form = CustomerProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_data(self):
        data = self.profile_data.copy()
        data['mobile'] = 'invalid-mobile-number'
        form = CustomerProfileForm(data=data)
        self.assertFalse(form.is_valid())

# Running the tests
if __name__ == '__main__':
    TestCase.main()
