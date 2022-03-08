from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class meta:
        model = Order
        field = ["order_by", "shipping_address", "mobile", "emial"]