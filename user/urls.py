# BookByte - Copyright (C) 2025 Keith Kk
# Licensed under GNU GPLv3. See LICENSE for details.

from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.ilogin, name='login'),
    path('logout/', views.ilogout, name='logout'),
    path('register/', views.iregister, name='register'),
    path('profile/', views.iprofile, name='profile'),
]