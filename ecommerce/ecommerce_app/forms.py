from django.contrib.auth.forms import UserCreationForm
from . models import Seller, Product
from django import forms

class SellerRegistrationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Seller.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username
    
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image size should not exceed 5MB.")
            if not image.content_type.startswith('image'):
                raise forms.ValidationError("Only image files are allowed.")
        return image

class Meta:
    model = Product 
    fields = ['name', 'description', 'price', 'image']
    error_messages = {
        'name': {
            'required': "Please enter a product name.",
        },
        'price': {
            'invalid': "Please enter a valid price.",
        },
        'image': {
            'invalid_image': "Please upload a valid image file.",
            'invalid_size': "Image size should nto exceed 5MB.",
        },
    }