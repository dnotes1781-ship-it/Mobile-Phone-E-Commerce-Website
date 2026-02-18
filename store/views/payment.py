from django.shortcuts import render, redirect
from store.models.product import Product
from store.models.customer import Customer

def payment_view(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('login')
        
    # Get products from cart
    is_buy_now = request.GET.get('source') == 'buynow'
    if is_buy_now:
        cart = request.session.get('buy_now_cart', {})
    else:
        cart = request.session.get('cart', {})
        
    if not cart:
        return redirect('store')

    ids = list(cart.keys())
    products = Product.get_products_by_id(ids)
    
    total_amount = sum(p.price * cart.get(str(p.id)) for p in products)
    customer = Customer.objects.get(id=customer_id)
    
    return render(request, 'payment.html', {
        'products': products,
        'total_amount': total_amount,
        'customer': customer,
        'is_buy_now': is_buy_now
    })
