# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

import re

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.http import require_POST


from .models import User, Profile

# Create your views here.

def check_password_validity(password):
    if len(password) < 6 or len(password)> 8:
        return False
    
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d',password):
        return False
    if not re.search(r'[^A-Za-z0-9\s]',password):
        return False
    
    return True



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

        if not check_password_validity(password):
            messages.error(request, f'Password must be 6–8 characters long and contain letters, numbers, and symbols!')
            return render (request,'user/register.html', context)


        if password != password2:
            messages.error(request,f'The passwords don\'t match!')
            return render (request, 'user/register.html')
        
        
        if User.objects.filter(email= context['email']).exists():
            messages.error(request, f'Email is already taken. Please use another!')
            return render(request,'user/register.html')
        
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


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ilogin(request):
    context = {'email': ''}

    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '')

        # Rate limiting
        client_ip = get_client_ip(request)
        cache_key = f"login_attempts_{client_ip}"
        attempts = cache.get(cache_key, 0)

        if attempts >= 5:  # Max 5 attempts per 15 mins
            messages.error(request,"Too many login attempts. Try again later.")
            return render(request,'user/login.html',context)

        # Authenticate
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active:
            login(request, user)
            cache.delete(cache_key)  # reset attempts
            messages.success(request, "Welcome! You are now logged in.")
            return redirect('index')
        else:
            cache.set(cache_key, attempts + 1, 900)  # 15 min lock
            messages.error(request, "Invalid email or password.")

        context['email'] = email

    return render(request, 'user/login.html', context)

@login_required
def ilogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def iprofile(request):
    return render (request, 'user/profile.html')