from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_book_club, name='create_book_club'),
    path('bookclubs/', views.book_club_list, name='book_club_list'),
    path('bookclub/<int:book_club_id>/', views.book_club_detail, name='book_club_detail'),
]