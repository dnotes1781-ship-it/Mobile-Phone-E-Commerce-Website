from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View


class userprofile(View):
    
  def get(self, request):
       
      email = request.POST.get('email')
      customer = request.session.get('customer')
      print("id is",customer)
      return render(request,'userprofile.html', {'customer' : customer})


  def post(self, request):
        postData = request.POST

        first_name = request.POST.get('first_name')
        print("id is",first_name)
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone
        }
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            print("mistyy....")
           
            request.session['customer'] = customer.id
            print( request.session['customer'] )
            # customer.password = make_password(customer.password)
            customer=Customer.objects.filter(id=customer.id).update(first_name=first_name,last_name=last_name,phone=phone,email=email)
            print("ss=",customer)
            return render(request, 'userprofile.html', {'error':'Your Profile Updated  Successfully..'})
      
        return render(request, 'userprofile.html', {'error': error_message})

       

   