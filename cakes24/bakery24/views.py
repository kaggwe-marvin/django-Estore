from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, Review
from .forms import Reviews


# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bakery24:signin')
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bakery24:shop')
        else:
            return HttpResponseBadRequest('Invalid login credentials.')
    else:
        return render(request, 'login.html')


def shop(request):
    url = reverse('bakery24:shop')
    products = Product.objects.all()
    context = {'url': url, 'products': products}
    return render(request, 'shop.html',context)

def checkout(request):
    url = reverse('bakery24:checkout')
    context = {'url': url}
    return render(request, 'checkout.html',context)

def payment(request):
    url = reverse('bakery24:payment')
    context = {'url': url}
    return render(request, 'payment.html',context)
    

def about(request):
    url = reverse('bakery24:about')
    if request.method == 'POST':
        form = Reviews(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'comments.html')
    else:
        form = Reviews()
    context = {'url': url, 'form':form}
    return render(request, 'about.html',context)

def cart(request):
    url = reverse('bakery24:cart')
    context = {'url': url}
    return render(request, 'cart.html',context)


def comments(request):
    url = reverse('bakery24:comments')
    reviewed = Review.objects.all().order_by('-id')
    context = {'url': url, 'reviewed':reviewed}
    return render(request, 'comments.html',context)

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart.products.add(product)
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart.products.remove(product)
    return redirect('cart')
@login_required
def view_cart(request):
    cart = request.user.cart
    products = cart.products.all()
    total_price = sum([product.price for product in products])
    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price,
    })

@login_required
def place_order(request):
    cart = request.user.cart
    products = cart.products.all()
    total_price = sum([product.price for product in products])
    order = Order.objects.create(user=request.user, total_price=total_price)
    for product in products:
        order.products.add(product)
    cart.products.clear()
    return redirect('checkout')
