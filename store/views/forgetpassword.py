from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import  View


class forgetpassword(View):
   
    def get(self , request):
       
        return render(request , 'forgetpassword.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        print("sjp",customer)

        error_message = None
        if customer:

            print(email, password)
            request.session['customer'] = customer.id
            print( request.session['customer'] )
            # customer.password = make_password(customer.password)
            password=make_password(password,hasher='default')
            customer=Customer.objects.filter(id=customer.id).update(password=password)
            
            return render(request, 'login.html', {})

            # flag = check_password(password, customer.password)
            
        else:
            error_message = 'Email id  invalid !!'

       
        return render(request, 'forgetpassword.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')
