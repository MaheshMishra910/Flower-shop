from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class meta:
        model = Order
        field = ["ordered_by", "shipping_address", "mobile", "email"]