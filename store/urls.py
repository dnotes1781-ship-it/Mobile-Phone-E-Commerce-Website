from django.contrib import admin
from django.urls import path
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.api import update_cart
from .views.checkout import CheckOut
from .views.orders import OrderView,some_view
from .views.contactus import contactus
from .views.aboutus import aboutus
from .views.product import product
from .views.details import product_detail
from .views.lenses import lenses
from .views.product import product
from .views.userprofile import userprofile
from .views.feedback import feedback
from .views.forgetpassword import forgetpassword
from .views.payment import payment_view
from .views.order_success import order_success
from .views.invoice import invoice_view
from .views.search import search_suggestions
from .views.buynow import BuyNow
from .views.bundle import AddBundle
from .views.chat import chat_api
from .middlewares.auth import  auth_middleware
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', Index.as_view(), name='homepage'),     # this is define as a class in home.py, so we need to call it as (name.as_view())
    path('store', store , name='store'),
   
    path('contactus', contactus.as_view(), name='contactus'),
    path('userprofile', userprofile.as_view(), name='userprofile'),
    path('feedback', feedback.as_view(), name='feedback'),
    #path('lenses', lenses , name='lenses'),
    path('aboutus', aboutus , name='aboutus'),
    #path('some_view', some_view , name='some_view'),
    path('product', product , name='product'),
    path('product/<int:id>', product_detail, name='product_detail'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('forgetpassword', forgetpassword.as_view(), name='forgetpassword'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('buy-now', BuyNow.as_view(), name='buy-now'),
    path('add-bundle', AddBundle.as_view(), name='add_bundle'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('payment', payment_view, name='payment'),
    path('order_success/<str:invoice_id>', order_success, name='order_success'),

    path('invoice/<str:invoice_id>', invoice_view, name='invoice'),
    path('search/suggestions', search_suggestions, name='search_suggestions'),
    path('api/update-cart', update_cart, name='update_cart'),
    path('api/chat', chat_api, name='chat_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
