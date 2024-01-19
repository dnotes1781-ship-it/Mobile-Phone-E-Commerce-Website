from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.contactus import Contactus        # import model from models
from django.views import  View


class contactus(View):
    
  def get(self, request):       # get is function for taking the data of users/customer...
       
      return render(request,'contactus.html')


  def post(self, request):
        postData = request.POST  # requested data will be post on server side...
        name = postData.get('name')
        email = postData.get('email')
        message = postData.get('message')
        # validation
        value = {
            'name': name,
            'email': email,
            'message':message
        }
        error_message = None

        contactus = Contactus(name=name,
                            email=email,
                            message=message
                           )
    
        if not error_message:
            print(name,  email, message)
            
            contactus.register()
            return render(request, 'contactus.html', {'error':'Your Message Added Successfully..'})
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'contactus.html', data)

   