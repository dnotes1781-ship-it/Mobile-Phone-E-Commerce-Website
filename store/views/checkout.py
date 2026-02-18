from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Product
from store.models.orders import Order


import uuid

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        bank_offer = request.POST.get('bank_offer')
        is_buy_now = request.POST.get('is_buy_now') == 'True'
        
        customer = request.session.get('customer')
        
        # Select Cart based on Source
        if is_buy_now:
            cart = request.session.get('buy_now_cart', {})
        else:
            cart = request.session.get('cart', {})
            
        products = Product.get_products_by_id(list(cart.keys()))
        
        invoice_id = str(uuid.uuid4())
        
        # Construct Full Address
        full_address = f"{address}, {city}, {state} - {zipcode}"

        # 1. Calculate Total Cart Value first
        total_cart_value = 0
        for product in products:
            qty = cart.get(str(product.id))
            total_cart_value += product.price * qty

        # 2. Calculate Total Discount
        total_discount = 0
        if bank_offer == 'HDFC':
            total_discount = int(total_cart_value * 0.10)
        elif bank_offer == 'SBI':
            if total_cart_value > 200:
                total_discount = 200

        # 3. Create Orders with Prorated Discount
        for product in products:
            qty = cart.get(str(product.id))
            price_total = product.price * qty
            
            # Weighted Discount
            if total_cart_value > 0:
                share = price_total / total_cart_value
                item_discount = total_discount * share
            else:
                item_discount = 0
            
            # Final price per unit for this order record
            final_price_per_unit = int((price_total - item_discount) / qty)

            status = 'Accepted' if request.POST.get('payment_mode') == 'Prepaid' else 'Pending'

            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=final_price_per_unit,
                          address=full_address,
                          phone=phone,
                          quantity=qty,
                          invoice_id=invoice_id,
                          status=status)
            order.save()
            
        # Clear the correct cart
        if is_buy_now:
            request.session['buy_now_cart'] = {}
        else:
            request.session['cart'] = {}

        return redirect(f'/order_success/{invoice_id}')

#        return redirect('https://dashboard.paytm.com/login/')
