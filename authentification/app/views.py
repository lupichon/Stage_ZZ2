from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from authentification import settings
from .token import generatorToken




# Create your views here.

def home(request):
    return render(request, "app/index.html")

def register(request):
    if request.method == "POST" : 
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request,'This username already exists')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request,'This email address is already in use by another account')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'The entered name is not correct')
            return redirect('register')
        if password != password1:
            messages.error(request, 'The two passwords do not match')
            return redirect('register')


        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()

        #envoi d'email de bienvenu
        messages.success(request, 'Your account has been successfully created')
        subject = "Welcome!"
        message = "Welcome " + my_user.first_name + " " + my_user.last_name + "\nWe are happy to have you with us\n\n\n Thank you! \n\n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject,message,from_email,to_list,fail_silently=False)

        #email de confirmation
        current_site = get_current_site(request)
        subject = "Confirmation of your email address"
        message = render_to_string("emailconfirm.html",{
            "name" : my_user.first_name,
            "domain" : current_site.domain,
            "uid" : urlsafe_base64_encode(force_bytes(my_user.pk)),
            "token" : generatorToken.make_token(my_user)
        })
        email = EmailMessage(email,message,settings.EMAIL_HOST_USER,[my_user.email])
        email.fail_silently = False
        email.send()
        return redirect('login')

    return render(request, "app/register.html")

def lOgin(request):
    if request.method == "POST" : 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        my_user = User.objects.get(username=username)
        if user is not None : 
            login(request, user)
            firstname = user.first_name
            return render(request, "app/index.html", {'firstname':firstname})
        elif my_user.is_active == False:
            messages.error(request,"The account is not yet activated")
            return redirect('login')
        else : 
            messages.error(request,'Invalid authentification, please try again later')
            return redirect('login')
    return render(request, "app/login.html")

def logOut(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('home')

def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generatorToken.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Your account has been activated")
        return redirect('login')
    else : 
        messages.error(request, "The activation of your account has failed")
        return redirect('home')