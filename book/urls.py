from . import views
from django.urls import path 
from django.contrib import admin

urlpatterns = [
    path ('', views.index, name='index'),
    path ('reader/', views.ireader, name='reader'),
    path ('upload_book/', views.upload_book, name='upload'),
    path ('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path ('read_book/<int:id>/', views.read_book, name='read_book'),
    path ('book_reading_progress/<int:id>/', views.book_reading_progress, name='reading_progress'),
]