from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Product
from store.models.orders import Order
from store.middlewares.auth import auth_middleware
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})


def some_view(request):

           
            buffer = io.BytesIO()

            
            p = canvas.Canvas(buffer,pagesize=letter,bottomup=0)
           
          
            textob = p.beginText()
            textob.setTextOrigin(inch, inch)
            textob.setFont("Helvetica", 14)
            customer = request.session.get('customer')
            orders=Order.get_orders_by_customer(customer)
            lines=[]

            for user in orders:
                lines.append(user.product)
                lines.append(user.quantity)
               
            for line in lines:
                textob.textLine(line)
               
            p.drawText(textob)
            p.showPage()
            p.save()            
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='hello.pdf') 


            