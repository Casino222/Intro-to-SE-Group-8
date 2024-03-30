from ecommerce_app.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.test import RequestFactory

def retrieveInventory(product_id):
    product = Product.objects.get(pk=product_id)
    inventory=product.stock
    return inventory

def retrieveCustomerFeedback(product_id):
    product = Product.objects.get(pk=product_id)
    comments = product.comments.all()
    feedback = [comment.content for comment in comments]
    return feedback

def addProduct(name, description, price, stock):
    product = Product.objects.create(name=name, description=description, price=price, stock=stock)
    return product

def editProduct(product_id, name=None, description=None, price=None, stock=None):
    product = Product.objects.get(pk=product_id)
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    product.save()
    return product

def removeProduct(product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()