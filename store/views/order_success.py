from django.shortcuts import render

def order_success(request, invoice_id):
    return render(request, 'order_success.html', {'invoice_id': invoice_id})
