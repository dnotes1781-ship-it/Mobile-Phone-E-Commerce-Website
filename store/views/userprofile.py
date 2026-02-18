from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View


class userprofile(View):
    
  def get(self, request):
       
      customer_id = request.session.get('customer')
      if customer_id:
          try:
            customer = Customer.objects.get(id=customer_id)
            print("id is", customer)
            return render(request, 'userprofile.html', {'customer': customer})
          except Customer.DoesNotExist:
             request.session.clear()
             return redirect('login')
      else:
          return redirect('login')


  def post(self, request):
        postData = request.POST

        first_name = request.POST.get('first_name')
        print("id is",first_name)
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
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
            customer=Customer.objects.filter(id=customer.id).update(first_name=first_name,last_name=last_name,phone=phone,email=email,address=address,city=city,state=state,zipcode=zipcode)
            
            # Re-fetch updated customer to show in form
            customer = Customer.objects.get(id=request.session.get('customer'))
            
            print("ss=",customer)
            return render(request, 'userprofile.html', {'success':'Your Profile Updated  Successfully..', 'customer': customer})
      
        return render(request, 'userprofile.html', {'error': error_message})

       

   