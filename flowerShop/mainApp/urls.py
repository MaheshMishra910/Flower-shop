from unicodedata import name
from django.urls import path
from .views import *
from . import views


app_name = "mainApp"
urlpatterns = [
    path("", HomeView.as_view(),name="home"),
    path("home", HomeView.as_view(),name="home"), 
    # path("ch/", views.get_context,name="ch"), #HomeView.as_view()
    # path("ch/", CheckoutView.get_context,name="ch"), #HomeView.as_view()
    path("contact/", contact, name="contact"),
    path("about/", AboutView.as_view(), name="about"),
    path("blog/", BlogView.as_view(),name="blog"),
    path("shop/",ShopView.as_view(), name="shop"),
    path("product/<slug:slug>/", ProductDetailView.as_view(),name="productdetail"),
    path("add-to-cart<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkoutsuccess/", CheckoutSuccessView.as_view(), name="checkoutsuccess"),
    path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
    path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),
    # path("register/", CustomerRegistrationView.as_view(), name="customerregistration"),
    path("register/", signup, name="customerregistration"),
    path("login/", view_authenticate_user, name="customerlogin"),
    # path("login/", CustomerLoginView.as_view(), name="customerlogin"),
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(), name="customerorderdetail"),
    path("search/", SearchView.as_view(), name="search"),
    path("add-to-wishlist<int:pro_id>/", AddToWishlistView.as_view(), name="addtowishlist"),
    path("wishlist/", MyWishListView.as_view(), name="mywishlist"),
    path("manage-wishlist/<int:cp_id>/", ManageWishlistView.as_view(), name="managewishlist"),
    path("add-to-compare<int:pro_id>/", AddToCompareView.as_view(), name="addtocompare"),
    path("compare/", MyCompareView.as_view(), name="mycompare"),
    path("manage-compare/<int:cp_id>/", ManageCompareView.as_view(), name="managecompare"),
    #admin side urls
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("adminlogout/", AdminLogoutView.as_view(), name="adminlogout"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="adminorderdetail"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-order-<int:pk>-change/", AdminOrderStatusChangeView.as_view(), name="adminorderstatuschange"),
    path("admin-product/list/", AdminProductListView.as_view(), name="adminproductlist"),
    path("admin-quick-message/list/", AdminQuickMessageView.as_view(), name="adminquickmessagelist"),
]