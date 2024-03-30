from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import transaction
from django.db.models import F
from .models import Product, Cart, Order

def add_to_cart(user_id, product_id, quantity):
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = cart.cart_items.get_or_create(product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity  
        cart_item.save()
        return True
    except ObjectDoesNotExist:
        return False

def calculate_total_price(user_id):
    try:
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
        total_price = Decimal(0)
        for cart_item in cart.cart_items.all():
            total_price += cart_item.product.price * cart_item.quantity 
        return total_price
    except ObjectDoesNotExist:
        return Decimal(0)

@transaction.atomic
def checkout(user_id, payment_method):
    try:
        user_cart = Cart.objects.get(user_id=user_id)
    except Cart.DoesNotExist:
        raise ValueError("User does not have a cart.")

    if not user_cart.cartitem_set.exists():
        raise ValueError("User's cart is empty.")

    for cart_item in user_cart.cartitem_set.all():
        if cart_item.quantity > cart_item.product.stock:
            raise ValueError(f"Insufficient stock for {cart_item.product.name}.")


    valid_payment_methods = ['Credit Card', 'PayPal', 'Stripe']
    if payment_method not in valid_payment_methods:
        raise ValueError("Invalid payment method.")

    total_price = sum(item.product.price * item.quantity for item in user_cart.cartitem_set.all())

    order = Order.objects.create(user=user_cart.user, payment_method=payment_method, total_price=total_price)

    for cart_item in user_cart.cartitem_set.all():
        cart_item.product.stock -= cart_item.quantity
        cart_item.product.save()

        order.products.add(cart_item.product)

    user_cart.cartitem_set.all().delete()

    return order

def send_email_notification(order):
    subject = 'Order Confirmation'

    message = render_to_string('email/notification_email.html', {'order': order})

    sender_email = 'your_email@example.com'

    recipient_email = order.user.email

    send_mail(subject, message, sender_email, [recipient_email])
