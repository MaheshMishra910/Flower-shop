from unicodedata import name
from django.urls import path
from .views import *


app_name = "mainApp"
urlpatterns = [
    path("", HomeView.as_view(),name="home"),
    path("home", HomeView.as_view(),name="home"),
    path("contact/", ContactView.as_view(),name="contact"),
    path("about/", AboutView.as_view(), name="about"),
    path("blog/", BlogView.as_view(),name="blog"),
    path("shop/",ShopView.as_view(), name="shop"),
    path("product/<slug:slug>/", ProductDetailView.as_view(),name="productdetail"),
    path("add-to-cart<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
]