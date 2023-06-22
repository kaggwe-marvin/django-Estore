from django.urls import path, include
from . import views
app_name = 'bakery24'
urlpatterns = [
 path('', include('django.contrib.auth.urls')),   
 path('', views.home, name='home'),
 path('about', views.about, name='about'),
 path('shop', views.shop, name='shop'),
 path('checkout', views.checkout, name='checkout'),
 path('payment', views.payment, name='payment'),
 path('signin', views.signin, name='signin'),
 path('cart', views.cart, name='cart'),
 path('comments', views.comments, name='comments'),
]