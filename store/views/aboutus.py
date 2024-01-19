from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View



    

def aboutus(request):
    
   return render(request,'aboutus.html')



