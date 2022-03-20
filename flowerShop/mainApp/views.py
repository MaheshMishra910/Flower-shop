from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CheckoutForm
from .models import *
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy


# Create your views here.


class HomeView(TemplateView):
    template_name = "index-2.html"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all().order_by("-id")[:8]
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


class ShopView(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Product.objects.all()
        return context


class ProductDetailView(TemplateView):
    template_name = "product-details-2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class AddToCartView(TemplateView):
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

class EmptyCartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mainApp:mycart")

class ManageCartView(View):
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



class MyCartView(TemplateView):
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

class CheckoutView(TemplateView):
    template_name = "checkout.html"
    from_class = CheckoutForm
    sucess_url = reverse_lazy("mainApp:home")

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
        return render(request, 'checkout.html')



class BlogView(TemplateView):
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
                    customer.full_name = fullname,
                    customer.address = address
                    customer.save()
                    messages.success(request,'You are registered!')
                    return redirect("mainApp:customerregistration")
        return render(request,"register.html")


def view_authenticate_user(request):
    if request.method == "GET": 
        return render(request, 'login.html') 
    else:
        print(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['pass']) 
        print(user)
        if user is not None:  
            login(request, user)
            messages.warning(request,'Login sucessfully')
            return redirect("mainApp:customerlogin")
            
        else: 
            messages.warning(request,'Please chek your username and password!!')
            return redirect("mainApp:customerlogin") 
