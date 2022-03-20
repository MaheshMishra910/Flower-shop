from unicodedata import name
from django.urls import path
from .views import *
from . import views


app_name = "mainApp"
urlpatterns = [
    path("", HomeView.as_view(),name="home"),
    path("home", HomeView.as_view(),name="home"), 
    # path("ch/", views.get_context,name="ch"), #HomeView.as_view()
    path("ch/", CheckoutView.get_context,name="ch"), #HomeView.as_view()
    path("contact/", ContactView.as_view(),name="contact"),
    path("about/", AboutView.as_view(), name="about"),
    path("blog/", BlogView.as_view(),name="blog"),
    path("shop/",ShopView.as_view(), name="shop"),
    path("product/<slug:slug>/", ProductDetailView.as_view(),name="productdetail"),
    path("add-to-cart<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    # path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("register/", signup, name="customerregistration"),
    path("login/", view_authenticate_user, name="customerlogin")
    # path("login/", CustomerLoginView.as_view(), name="customerlogin"),
]