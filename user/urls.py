from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.ilogin, name='login'),
]