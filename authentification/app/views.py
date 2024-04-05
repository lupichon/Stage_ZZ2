from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, "app/index.html")

def register(request):
    #on récupère ce qui a été entré par l'utilisateur
    if request.method == "POST" : 
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username):
            messages.error(request,'Cet utilisateur existe déjà')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request,'Cet email est déjà utilisée')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'Le nom entré n est pas correct ')
            return redirect('register')
        if password != password1:
            messages.error(request, 'Les deux mots de passe ne coincident pas')
            return redirect('register')


        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()
        messages.success(request, 'Votre compte compte a été créé avec succés')
        return redirect('login')

    return render(request, "app/register.html")

def lOgin(request):
    if request.method == "POST" : 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None : 
            login(request, user)
            firstname = user.first_name
            return render(request, "app/index.html", {'firstname':firstname})
        else : 
            messages.error(request,'Mauvaise authentification')
            return redirect('login')
    return render(request, "app/login.html")

def logOut(request):
    logout(request)
    messages.success(request, "Vous avez été bien déconnécté")
    return redirect('home')