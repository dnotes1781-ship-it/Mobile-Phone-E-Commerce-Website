from django.http import JsonResponse
from store.models.product import Product

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        
        if not cart:
            cart = {}
            
        quantity = cart.get(product_id)
        
        if quantity:
            if remove:
                if quantity <= 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1
        else:
            cart[product_id] = 1
            
        request.session['cart'] = cart
        
        # Calculate total items for badge
        total_items = len(cart.keys())
        
        return JsonResponse({
            'status': 'success',
            'cart_length': total_items,
            'product_qty': cart.get(product_id, 0)
        })
        
    return JsonResponse({'status': 'fail'}, status=400)
