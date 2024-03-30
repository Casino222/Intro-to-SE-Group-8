from django.urls import path
from ecommerce_app import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),  
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),   
    path('search/', views.search_view, name='search'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('seller/register/', views.seller_register, name='seller_register'),  
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller/add_product/', views.add_product, name='add_product'),
    path('seller/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller/orders/', views.seller_order_list, name='seller_order_list'),
    path('seller/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'), 
]
