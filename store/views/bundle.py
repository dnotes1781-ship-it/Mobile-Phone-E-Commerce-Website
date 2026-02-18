from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from store.models.product import Product

class AddBundle(View):
    def post(self, request):
        product_ids_str = request.POST.get('product_ids')
        if product_ids_str:
            product_ids = product_ids_str.split(',')
            cart = request.session.get('cart', {})
            
            for product_id in product_ids:
                if product_id:
                    # Check if valid integer
                    try:
                        pid = str(int(product_id)) # Validation + standard format
                        if pid in cart:
                            cart[pid] += 1
                        else:
                            cart[pid] = 1
                    except ValueError:
                        continue
            
            request.session['cart'] = cart
            messages.success(request, "Bundle added to cart successfully!")
            
        return redirect(request.META.get('HTTP_REFERER', 'homepage'))
