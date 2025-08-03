# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

from django.shortcuts import render,redirect,get_list_or_404
from django.contrib import messages
from .models import User, Profile
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.
def iregister(request):
    context = {
        'username': '',
        'email':'',
        'password':'',
        'password2':'',
    }
    if request.method == 'POST':
        context['username']  = request.POST.get('username')
        context['email'] = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request,f'The passwords don\'t match!')
            return render (request, 'user/register.html')
        
        if User.objects.filter(email= context['email']).exists():
            messages.error(request, f'Email is already taken. Please use another!')
            return render(request,'users/register.html')
        
        user = User.objects.create(
            username = context['username'],
            email = context['email'],
        )

        user.set_password(password)
        user.is_active = True
        user.save()
        messages.success(request, f'Account created successfully! You can now login.')
        return redirect('login')
        
    return render (request,'user/register.html',context)


def ilogin(request):

    context = {
        'email': '',
    }
    if request.method == 'POST':
        context['email'] = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,username = context['email'], password=password
        )

        if user is not None:
            login(request,user)
            messages.success(request,f'Welcome, {context['email']}!')
            return redirect('index')
        else:
            if User.objects.filter(email = context['email']).exists():
                messages.error(request,f'Invalid credentials provided!')
            else:
                messages.error(request, f'Account with the email does not exist.')
            return redirect('login')

    return render (request,'user/login.html', context)

def ilogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def iprofile(request):
    return render (request, 'user/profile.html')