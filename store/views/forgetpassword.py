from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
import random

class forgetpassword(View):
    def get(self, request):
        return render(request, 'forgetpassword.html', {'step': 'email'})

    def post(self, request):
        action = request.POST.get('action')
        
        # Step 1: Validate Email and Send OTP
        if action == 'validate_email':
            email = request.POST.get('email')
            customer = Customer.get_customer_by_email(email)
            
            if customer:
                # Generate OTP
                otp = random.randint(1000, 9999)
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email
                
                # Send OTP
                subject = 'Password Reset OTP'
                message = f'Your OTP for password reset is {otp}.'
                email_from = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@eshop.com'
                recipient_list = [email]
                
                try:
                    send_mail(subject, message, email_from, recipient_list)
                    print(f"OTP Sent to {email}: {otp}") # Console log for verification
                    return render(request, 'forgetpassword.html', {'step': 'otp', 'email': email, 'success': f'OTP sent to {email}'})
                except Exception as e:
                    print(e)
                    return render(request, 'forgetpassword.html', {'step': 'email', 'error': 'Failed to send OTP. Try again.'})
            else:
                return render(request, 'forgetpassword.html', {'step': 'email', 'error': 'Email ID not registered. Please sign up.'})

        # Step 2: Verify OTP and Reset Password
        elif action == 'reset_password':
            email = request.POST.get('email')
            otp_input = request.POST.get('otp')
            new_password = request.POST.get('password')
            
            session_otp = request.session.get('reset_otp')
            session_email = request.session.get('reset_email')
            
            # Verify OTP
            if str(session_otp) == str(otp_input) and session_email == email:
                # Reset Password
                hashed_password = make_password(new_password)
                Customer.objects.filter(email=email).update(password=hashed_password)
                
                # Clear Session
                if 'reset_otp' in request.session:
                    del request.session['reset_otp']
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                    
                return render(request, 'login.html', {'success': 'Password reset successful! Please login.'}) # Using error key for login page alert style to be consistent, or could use success if supported
            else:
                 return render(request, 'forgetpassword.html', {'step': 'otp', 'email': email, 'error': 'Invalid OTP. Please try again.'})
        
        return redirect('forgetpassword')

