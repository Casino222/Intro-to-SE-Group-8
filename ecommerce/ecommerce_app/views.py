from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . utils import retrieveInventory, retrieveCustomerFeedback
from ecommerce_app.models import Product
from django.contrib.auth import login
from . search import search_products
from . models import Product, Order, OrderStatus
from . forms import SellerRegistrationForm, ProductForm
from . order_management import (
    view_order_history,
    track_order_status
)
from . purchase import (
    calculate_total_price,
    checkout,
    send_email_notification,
)





def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    filters = request.GET.dict() 

    results = search_products(query, category, filters)
    return render(request, 'search_results.html', {'results': results})

@login_required
def cart_view(request):
    cart_items = request.user.cart_items.all()
    total_price = calculate_total_price(request.user.id)
    return render(request, 'cart_checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout_view(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order = checkout(request.user.id, payment_method)
        if order:
            send_email_notification(order)
            return redirect('order_confirmation')
        else:
            return redirect('checkout_error')
    else:
        return render(request, 'cart_checkout.html')

@login_required
def order_history(request):
    orders = view_order_history(request.user)
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def track_order(request, order_id):
    status = track_order_status(order_id)
    return render(request, 'track_order.html', {'status': status})

def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller_login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'sellers/seller_register.html', {'form': form})

def seller_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('seller_dashboard')
        else:
            form = AuthenticationForm()
        return render(request, 'sellers/seller_login.html', {'form': form})
    
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('seller_dahsboard')
    else:
        form = ProductForm()
    return render(request, 'seller_login.html', {'form': form})

def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sellers/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('seller_dashboard')

def seller_order_list(request):
    pending_orders = Order.objects.filter(status='PENDING')
    return render(request, 'sellers/order_list.html', {'orders': pending_orders})


@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

        OrderStatus.objects.create(order=order, status=new_status)
        return redirect('seller_order_list')
    else:
        order = Order.objects.get(id=order_id)
        return render(request, 'update_order_status.html', {'order': order})


def inventory_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    inventory = retrieveInventory(product_id)
    return render(request, 'inventory.html', {'product': product, 'inventory': inventory})

def feedback_view(request, product_id):
    product = Product.objects.get(pk=product_id)
    feedback = retrieveCustomerFeedback(product_id)
    return render(request, 'feedback.html', {'product': product, 'feedback': feedback})
