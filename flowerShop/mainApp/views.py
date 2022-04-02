from msilib.schema import ListView
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView, DetailView, ListView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CheckoutForm
from .models import *
from .forms import *
from .models import User
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()

        return super().dispatch(request, *args, **kwargs)

class HomeView(EcomMixin, TemplateView):
    template_name = "index-2.html"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")[:8]
        context['featured_product'] = Product.objects.all().order_by("id")[:6]
        return context
    

# def get_context(request):
#     if request.method == 'POST':
#         order = Order()
#         full_name = request.POST['fname']
#         address = request.POST['address']
#         phone = request.POST['pnumber']
#         memail = request.POST['femail']

#         order.ordered_by = full_name
#         order.email = memail
#         order.shipping_address = address
#         order.mobile = phone
#         cart_id = request.session.get("cart_id")
#         if cart_id:
#             cart_obj = Cart.objects.get(id=cart_id)
#             order.cart = cart_obj
#             order.subtotal = cart_obj.total
#             order.discount = 0
#             order.total = cart_obj.total
#             order.order_status = "Order Received"
#             del request.session['cart_id']  
#             order.save()
		
#     return render(request, 'checkout.html')

    


class ContactView(TemplateView):
    template_name = "contact-us.html"
    

class AboutView(TemplateView):
    template_name = "about-us.html"


class ShopView(EcomMixin, TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['allcategories'] = product_list
        return context


class ProductDetailView(EcomMixin, TemplateView):
    template_name = "product-details-2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class AddToCartView(EcomMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #for get product id from requested url
        product_id = self.kwargs['pro_id']
        #for get product
        product_obj = Product.objects.get(id=product_id)
        #for cart ma aagadi xavane check garne
        cart_id = self.request.session.get("cart_id",None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)
            
            #for items already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_prince
                cartproduct.save()
                cart_obj.total += product_obj.selling_prince
                cart_obj.save()
                
            #for new item id added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
                cart_obj.total += product_obj.selling_prince
                cart_obj.save()


        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
            cart_obj.total += product_obj.selling_prince
            cart_obj.save()

        return context

class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mainApp:mycart")

class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        
        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
            
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect("mainApp:mycart")



class MyCartView(EcomMixin, TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class AddToWishlistView(EcomMixin, TemplateView):
    template_name = "addtowishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #for get product id from requested url
        product_id = self.kwargs['pro_id']
        #for get product
        product_obj = Product.objects.get(id=product_id)
        #for cart ma aagadi xavane check garne
        wishlist_id = self.request.session.get("wishlist_id",None)
        if wishlist_id:
            wishlist_obj = Wishlist.objects.get(id=wishlist_id)
            this_product_in_wishlist = wishlist_obj.wishlistproduct_set.filter(
                product=product_obj)
            
            #for items already exists in cart
            #for items already exists in cart
            if this_product_in_wishlist.exists():
                wishlistproduct = this_product_in_wishlist.last()
                wishlistproduct.quantity += 1
                wishlistproduct.subtotal += product_obj.selling_prince
                wishlistproduct.save()
                wishlist_obj.total += product_obj.selling_prince
                wishlist_obj.save()
                
            #for new item id added in cart
            else:
                wishlistproduct = WishlistProduct.objects.create(
                    wishlist=wishlist_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
                wishlist_obj.total += product_obj.selling_prince
                wishlist_obj.save()


        else:
            wishlist_obj = Wishlist.objects.create(total=0)
            self.request.session['wishlist_id'] = wishlist_obj.id
            wishlistproduct = WishlistProduct.objects.create(
                    wishlist=wishlist_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
            wishlist_obj.total += product_obj.selling_prince
            wishlist_obj.save()

        return context
class ManageWishlistView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = WishlistProduct.objects.get(id=cp_id)
        wishlist_obj = cp_obj.wishlist
        
        if action == "rmv":
            wishlist_obj.total -= cp_obj.subtotal
            wishlist_obj.save()
            cp_obj.delete()
            
        else:
            pass

        return redirect("mainApp:mywishlist")

class MyWishListView(TemplateView):
    template_name = "wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist_id = self.request.session.get("wishlist_id", None)
        if wishlist_id:
            wishlist = Wishlist.objects.get(id=wishlist_id)
        else:
            wishlist = None
        context['wishlist'] = wishlist
        return context

class AddToCompareView(EcomMixin, TemplateView):
    template_name = "addtocompare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #for get product id from requested url
        product_id = self.kwargs['pro_id']
        #for get product
        product_obj = Product.objects.get(id=product_id)
        #for cart ma aagadi xavane check garne
        compare_id = self.request.session.get("compare_id",None)
        if compare_id:
            compare_obj = Compare.objects.get(id=compare_id)
            this_product_in_compare = compare_obj.compareproduct_set.filter(
                product=product_obj)
            
            #for items already exists in cart
            if this_product_in_compare.exists():
                compareproduct = this_product_in_compare.last()
                compareproduct.save()
                
            #for new item id added in cart
            else:
                compareproduct = CompareProduct.objects.create(
                    compare=compare_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
                compare_obj.total += product_obj.selling_prince
                compare_obj.save()


        else:
            compare_obj = Compare.objects.create(total=0)
            self.request.session['compare_id'] = compare_obj.id
            compareproduct = CompareProduct.objects.create(
                    compare=compare_obj, product=product_obj, rate=product_obj.selling_prince, quantity=1, subtotal=product_obj.selling_prince
                )
            compare_obj.total += product_obj.selling_prince
            compare_obj.save()

        return context
class ManageCompareView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CompareProduct.objects.get(id=cp_id)
        compare_obj = cp_obj.compare
        
        if action == "rmv":
            compare_obj.total -= cp_obj.subtotal
            compare_obj.save()
            cp_obj.delete()
            
        else:
            pass

        return redirect("mainApp:mycompare")
class MyCompareView(EcomMixin, TemplateView):
    template_name = "compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compare_id = self.request.session.get("compare_id", None)
        if compare_id:
            compare = Compare.objects.get(id=compare_id)
        else:
            compare = None
        context['compare'] = compare
        return context

class CheckoutView(EcomMixin, TemplateView):
    template_name = "checkout.html"
    # from_class = CheckoutForm
    # sucess_url = reverse_lazy("mainApp:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/checkout")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    # def form_valid(self, form):
    #     cart_id = self.request.session.get("cart_id")
    #     if cart_id:
    #         cart_obj = Cart.objects.get(id=cart_id)
    #         form.instance.cart = cart_obj
    #         form.instance.subtotal = cart_obj.total
    #         form.instance.discount = 0
    #         form.instance.total = cart_obj.total
    #         form.instance.order_status = "Order Received"
    #         del self.request.session['cart_id']   
    #     else: 
    #         return redirect("mainApp:home")
    #     return super().form_valid(form)


    def get_context(request):
        if request.method == 'POST':
            order = Order()
            full_name = request.POST['fname']
            address = request.POST['address']
            phone = request.POST['pnumber']
            memail = request.POST['femail']

            order.ordered_by = full_name
            order.email = memail
            order.shipping_address = address
            order.mobile = phone
            cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            order.cart = cart_obj
            order.subtotal = cart_obj.total
            order.discount = 0
            order.total = cart_obj.total
            order.order_status = "Order Received"
            del request.session['cart_id']  
            order.save()
            messages.success(request,'Your order sucessfully done')
            return redirect("mainApp:home")
            
        return render(request, 'checkout.html')



class BlogView(EcomMixin, TemplateView):
    template_name = "blog.html"

# class CustomerRegistrationView(TemplateView):
#     template_name = "register.html"

#     def signup(request):
#         if request.method == 'POST':
#             username = request.POST['username']
#             fullname = request.POST['fullname']
#             email = request.POST['email']
#             address = request.POST['address']
#             password = request.POST['pass']
#             cpassword = request.POST['cpass']
            
#             if password == cpassword:
#                 if User.objects.filter(username = username).exists():
#                     messages.error(request,'The username is already taken')
#                     return redirect("mainApp:customerregistration")
#                 elif User.objects.filter(email = email).exists():
#                     messages.error(request,'The email is already taken')
#                     return redirect("mainApp:customerregistration")
#                 else:
#                     user = User.objects.create_user(
# 					username = username,
# 					email = email,
# 					password = password
# 					)
#                     user.save()

#                     customer = Customer.objects.create_user(
#                         full_name = fullname,
#                         address = address
#                     )
#                     customer.save()
#                     messages.success(request,'You are registered!')
#                     return redirect("mainApp:customerregistration")
#         return render(request,"mainApp:customerregistration")

def signup(request):
        if request.method == 'POST':
            username = request.POST['username']
            fullname = request.POST['fullname']
            email = request.POST['email']
            address = request.POST['address']
            password = request.POST['pass']
            cpassword = request.POST['cpass']
            
            if password == cpassword:
                if User.objects.filter(username = username).exists():
                    messages.error(request,'The username is already taken')
                    return redirect("mainApp:customerregistration")
                elif User.objects.filter(email = email).exists():
                    messages.error(request,'The email is already taken')
                    return redirect("mainApp:customerregistration")
                else:
                    user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
                    user.save()
                
                    customer = Customer()
                    customer.user = User.objects.get(username=user)
                    customer.full_name = fullname
                    customer.address = address
                    customer.save()
                    messages.success(request,'You are registered!')
                    return redirect("mainApp:customerlogin")
        return render(request,"register.html")


def view_authenticate_user(request):
    if request.method == "GET": 
        return render(request, 'login.html') 
    else:
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['pass']) 
        print(user)
        if user is not None and Customer.objects.filter(user=user).exists():  
            login(request, user)
            messages.warning(request,'Login sucessfully')
            # if "next" in request.GET:
            #     next_url = request.GET.get("next")
            #     return next_url
            # else:
            #     return redirect("mainApp:customerlogin")

            return redirect("mainApp:home")   
            
        else: 
            messages.warning(request,'Please chek your username and password!!')
            return redirect("mainApp:customerlogin") 

class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("mainApp:home")

class CustomerProfileView(TemplateView):
    template_name = "my-account.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context["customer"] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetails.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer: #authenticated for other customer ordered details
                return redirect("mainApp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(title__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context

#for admin pages

class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = AdminLoginView
    success_url = reverse_lazy("mainApp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Incorrect username and password"})


        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)

class AdminLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("mainApp:adminhome")


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(order_status="Order Received")

        return context

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "order_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("mainApp:adminorderdetail", kwargs={"pk": self.kwargs["pk"]}))

