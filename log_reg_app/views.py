from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=pw_hash,
        )
    
    #Log in the user and redirect to success
    request.session['user_id']=user.id
    return redirect('/success')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
    
    messages.error(request,'Invalid Email/Password combination')
    return redirect("/")

def success(request):
    context={
        'user':User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'success.html', context)
