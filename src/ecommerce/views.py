from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import View,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from user.models import Customer
from .models import Product,ProductImg,ProductProperty,productComment,Cart,Gallery,Order
from .forms import ProductComment,AddNewAddressForm
# Create your views here.

def home(request):
    return render(request,'ecommerce/home.html')

def index(request):
    return render(request,'ecommerce/index.html')

class CatalogView(ListView):
    model = Product
    template_name = 'ecommerce/catalog.html'
    context_object_name = 'products'
    paginate_by = 6
    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            item_in_cart = Product.objects.filter(cart__user =self.request.user)
        else:
            item_in_cart = []
        context = super(CatalogView, self).get_context_data(**kwargs)
        context['item_in_cart'] = item_in_cart
        return context
    
@login_required(login_url='login')
def favorite_or_unfavorite(request):
    id = request.GET.get('id',None)
    user = request.user
    product = Product.objects.get(id=id)
    
    if user in product.favourites.all():
        product.favourites.remove(user)
    else:
        product.favourites.add(user)
    data={
        'id':id
    }
    return JsonResponse(data)

class ProductFilterView(ListView):
    def get(self, request, *args, **kwargs):
        types = request.GET.getlist('type[]')
        screens = request.GET.getlist('screen[]')
        scr = request.GET.getlist('scrManufacturereen[]')
        tags = request.GET.get('tags' or None)
        price = request.GET.get('price')
        listby = request.GET.get('listby')
        allproducts = Product.objects.all()
        if listby:
            allproducts = allproducts.order_by(listby).distinct()
        if len(types)>0:
            allproducts = allproducts.filter(prodtype__in=types).distinct()
        if len(screens)>0:
            allproducts = allproducts.filter(screen_size__in=screens).distinct()
        if len(scr)>0:
            allproducts = allproducts.filter(Brand__in=scr).distinct()
        if tags:
            allproducts = allproducts.filter(tag1=tags)
        if price:
            allproducts = allproducts.filter(selling_price__lte=price)
        if request.user.is_authenticated:
            item_in_cart = Product.objects.filter(cart__user =self.request.user)
        else:
            item_in_cart =[]
        paginator = Paginator(allproducts, 6)

        page_number = request.GET.get('pag')
        page_obj = paginator.get_page(page_number)
        context = {
        'products':allproducts,
        'item_in_cart':item_in_cart,
        'page_obj':page_obj,
        }
        t = render_to_string('ecommerce/products.html',context)
        data = {
            'data':t,
            
        }
        return JsonResponse(data)

class CatalogProductView(View):
    def get(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        images = ProductImg.objects.filter(product=pk)
        props = ProductProperty.objects.filter(product=pk)
        comments = productComment.objects.filter(product=pk)
        recom = Product.objects.all().order_by('-id')[:4]
        cou = images.count() + 1
        form = ProductComment()
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(user=request.user,product=product).exists()
        else:
            item_in_cart = False
        context = {
            'product':product,
            'images':images,
            'props':props,
            'comments':comments,
            'recom':recom,
            'cou':cou,
            'form':form,
            'item_in_cart':item_in_cart
        }
        return render(request,'ecommerce/catalog-product.html',context)
    def post(self,request,pk):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(f'/account/login/?next=/catalogproduct/{pk}')
        product = Product.objects.get(pk=pk)
        user = request.user
        form = ProductComment(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = user
            form_save.product = product
            form_save.save()
            messages.success(request,'added comment successfully!!')
            return redirect('catalog-product',pk=product.pk)

@login_required(login_url='login')
def add_to_cart(request):
    if request.method =='POST':
        user= request.user
        product = Product.objects.get(pk=request.POST.get('id'))
        Cart.objects.create(user=user,product=product)
        return redirect('catalog-product',pk=product.pk)

class CartView(LoginRequiredMixin,View):
    def get(self,request):
        user = request.user
        carts = Cart.objects.filter(user=user)
        cartlist = [p for p in Cart.objects.all() if p.user == user]
        total_amount = 0.0
        for p in cartlist:
                total_amount += p.amount
        context = {
            'carts':carts,
            'total_amount':total_amount
            }
        return render(request,'ecommerce/cart.html',context)

@login_required(login_url='login')
def plus_or_minus_cart(request):
    state =request.GET.get('state')
    cart_id = request.GET.get('id')
    user = request.user
    cart = Cart.objects.get(pk=cart_id,user=user)
    if state == 'plus':
        cart.quantity += 1
        cart.save()
    if state == 'minus':
        if not cart.quantity == 1:
            cart.quantity -= 1
            cart.save()
    cartlist = [p for p in Cart.objects.all() if p.user == user]
    total_amount = 0.0
    for p in cartlist:
            total_amount += p.amount
    data = {
        'cart_quantity':cart.quantity,
        'cart_amount':cart.amount,
        'total_amount':total_amount
    }
    return JsonResponse(data)

@login_required(login_url='login')
def remove_cart(request):
    cart_id = request.GET.get('id')
    Cart.objects.get(pk=cart_id,user=request.user).delete()
    cart_count = Cart.objects.filter(user=request.user).count()
    cartlist = [p for p in Cart.objects.all() if p.user == request.user]
    total_amount = 0.0
    for p in cartlist:
        total_amount += p.amount
    data = {
        'total_amount':total_amount,
        'cart_count':cart_count,
    }
    return JsonResponse(data)

class GalleryView(View):
    def get(self,request):
        gallerys = Gallery.objects.all()
        context={
            'gallerys':gallerys
        }
        return render(request,'ecommerce/gallery.html',context)

class CheckoutView(LoginRequiredMixin,View):
    def get(sellf,request):
        cart = Cart.objects.filter(user=request.user)
        Delivery = 10
        total_amount = 0
        for p in cart:
            total_amount += p.amount
        form = AddNewAddressForm()
        customer = Customer.objects.filter(user=request.user)
        context = {
            'cart':cart,
            'Delivery':Delivery,
            'all_amount':total_amount,
            'total_amount':total_amount + Delivery,
            'cart':cart,
            'form':form,
            'customer':customer
        }
        return render(request,'ecommerce/checkout.html',context)
    def post(self,request):
        if 'CustCountry' in request.POST:
            form = AddNewAddressForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit=False)
                form_save.user = request.user
                form_save.save()
                return redirect('checkout')
        
@login_required(login_url='login')
def payment_done(request):
    cart = Cart.objects.filter(user=request.user)
    address = request.POST['address']
    option = request.POST['option']
    payment = request.POST['payment']
    remark = request.POST['remark']
    cusom = Customer.objects.get(pk=address)
    for c in cart:
        Order(user=request.user,product=c.product,quantity=c.quantity,location=cusom,delevery_option=option,payment=payment,remark=remark).save()
        c.delete()
    return redirect('profile',username=request.user)