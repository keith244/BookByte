from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.ilogin, name='login'),
    path('logout/', views.ilogout, name='logout'),
    path('register/', views.iregister, name='register'),
    path('profile/', views.iprofile, name='profile'),
]