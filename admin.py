#admin.py
from django.contrib import admin
from . models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
from .models import SellerRequest
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products','quantity']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin): 
    list_display=['id','user','customers','products','quantity','ordered_date','status','payments']
    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)

    def products(self,obj):
        link=reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

    def payments(self,obj):
        link=reverse('admin:app_payment_change',args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link, obj.product.title)
    
class SellerRequestAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'status']
    actions = ['approve_requests', 'decline_requests', 'pending_request']

    def user_profile(self, obj):
        return obj.user.get_full_name()  # Assuming user has a full name field

    def approve_requests(self, request, queryset):
        for request in queryset:
            if request.status != 'approved':
                request.status = 'approved'
                request.save()
                request.user.is_staff = True
                request.user.save()

    def decline_requests(self, request, queryset):
        for request in queryset:
            if request.status != 'declined':
                request.status = 'declined'
                request.save()

    def pending_request(self, request, queryset):
        pending_queryset = queryset.filter(status='pending')
        if pending_queryset.exists():
            self.message_user(request, f"{pending_queryset.count()} pending requests found.")
        else:
            self.message_user(request, "No pending requests.")

    pending_request.short_description = "Mark selected as pending requests"

admin.site.register(SellerRequest, SellerRequestAdmin)

admin.site.unregister(Group)