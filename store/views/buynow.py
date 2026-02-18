from django.shortcuts import redirect
from django.views import View
from store.models.product import Product

class BuyNow(View):
    def post(self, request):
        product_id = request.POST.get('product')
        
        # Create a dedicated single-item cart for Buy Now
        buy_now_cart = {}
        buy_now_cart[product_id] = 1
        
        # Save to session
        request.session['buy_now_cart'] = buy_now_cart
        
        # Redirect directly to payment page with source flag
        return redirect('/payment?source=buynow')
