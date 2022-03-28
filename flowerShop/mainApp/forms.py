from django import forms
from .models import Order, Customer, Product
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class meta:
        model = Order
        field = ["ordered_by", "shipping_address", "mobile", "email"]

class AdminLoginView(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())