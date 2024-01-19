from django.shortcuts import render , redirect , HttpResponseRedirect

from django.contrib.auth.hashers import  check_password
from store.models.feedback import Feedback
from django.views import  View


class feedback(View):
    
  def get(self, request):
       
      return render(request,'feedback.html')


  def post(self, request):
        postData = request.POST
        
        email = postData.get('email')
        message = postData.get('message')
        # validation
        value = {
           
            'email': email,
            'message':message
        }
        error_message = None

        feedback = Feedback(email=email,
                            message=message
                           )
        

        if not error_message:
            print(email, message)
            
            feedback.register()
            return render(request, 'feedback.html', {'error':'Your Feedback Added Successfully..'})
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'feedback.html', data)

   