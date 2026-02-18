from django.shortcuts import render
from store.models.orders import Order
from django.db.models import Sum

def invoice_view(request, invoice_id):
    orders = Order.objects.filter(invoice_id=invoice_id)
    
    if not orders.exists():
        return render(request, 'index.html') # Or 404
        
    total_amount = sum(order.price * order.quantity for order in orders)
    original_total = sum(order.product.price * order.quantity for order in orders)
    total_discount = original_total - total_amount
    
    first_order = orders.first()
    customer = first_order.customer
    date = first_order.date
    address = first_order.address
    
    return render(request, 'invoice.html', {
        'orders': orders,
        'total_amount': total_amount,
        'original_total': original_total,
        'total_discount': total_discount,
        'invoice_id': invoice_id,
        'customer': customer,
        'date': date,
        'address': address
    })
